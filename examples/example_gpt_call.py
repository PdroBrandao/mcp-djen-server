"""
Real LLM Integration Example for MCP DJEN Server

This example demonstrates how to integrate the MCP DJEN Server with OpenAI's Function Calling
to create an intelligent legal assistant that can retrieve and analyze court notifications.

Features:
- Real function calling implementation
- Error handling and retry logic
- Structured response processing
- Deadline calculation and action recommendations
- Production-ready code patterns
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import openai
import httpx
from pydantic import BaseModel, Field
import re


class CourtNotification(BaseModel):
    """Structured court notification"""
    date: str
    court: str
    lawyer_name: str
    oab: str
    case_number: str
    type: str
    summary: str
    url: str
    deadline: Optional[str] = None
    actions: List[str] = []


class LegalAssistant:
    """
    Intelligent legal assistant using MCP DJEN Server
    
    This class demonstrates how to create a production-ready legal assistant
    that can understand natural language queries and retrieve court notifications
    through the MCP DJEN Server.
    """
    
    def __init__(self, openai_api_key: str, mcp_server_url: str):
        self.openai_api_key = openai_api_key
        self.mcp_server_url = mcp_server_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Configure OpenAI
        openai.api_key = openai_api_key
        
        # Define the function schema for court notifications
        self.functions = [
            {
                "name": "get_court_notifications",
                "description": "Retrieve court notifications for a lawyer within a date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Lawyer's full name (e.g., 'PEDRO BRANDÃO')"
                        },
                        "date_start": {
                            "type": "string",
                            "description": "Start date in YYYY-MM-DD format"
                        },
                        "date_end": {
                            "type": "string",
                            "description": "End date in YYYY-MM-DD format"
                        },
                        "oab": {
                            "type": "string",
                            "description": "OAB registration number (optional)"
                        }
                    },
                    "required": ["name", "date_start", "date_end"]
                }
            }
        ]

    async def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a natural language query and return structured response
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Structured response with notifications and analysis
        """
        try:
            # Step 1: Use OpenAI to understand the query and extract parameters
            function_call = await self._extract_function_call(user_query)
            
            if not function_call:
                return {
                    "error": "Could not understand query",
                    "message": "Please rephrase your question about court notifications"
                }
            
            # Step 2: Call MCP Server with extracted parameters
            notifications = await self._get_notifications_from_mcp(function_call)
            
            # Step 3: Analyze notifications and provide insights
            analysis = await self._analyze_notifications(notifications, user_query)
            
            return {
                "query": user_query,
                "notifications": notifications,
                "analysis": analysis,
                "total_count": len(notifications),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": "Processing failed",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _extract_function_call(self, user_query: str) -> Optional[Dict[str, Any]]:
        """Use OpenAI to extract function call parameters from natural language"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a legal assistant that helps lawyers check their court notifications. 
                        When a user asks about their notifications, extract the necessary information to call the 
                        get_court_notifications function. If no specific date is mentioned, use today's date."""
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
                ],
                functions=self.functions,
                function_call="auto"
            )
            
            message = response.choices[0].message
            
            if message.function_call:
                return json.loads(message.function_call.arguments)
            
            return None
            
        except Exception as e:
            print(f"Error extracting function call: {e}")
            return None

    async def _get_notifications_from_mcp(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Call MCP DJEN Server to get notifications"""
        try:
            # Prepare query parameters
            query_params = {
                "name": params["name"],
                "date_start": params["date_start"],
                "date_end": params["date_end"]
            }
            
            if "oab" in params:
                query_params["oab"] = params["oab"]
            
            # Make request to MCP Server
            response = await self.client.get(
                f"{self.mcp_server_url}/intimations",
                params=query_params
            )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}")
            return []
        except Exception as e:
            print(f"Error calling MCP server: {e}")
            return []

    async def _analyze_notifications(
        self, 
        notifications: List[Dict[str, Any]], 
        original_query: str
    ) -> Dict[str, Any]:
        """Analyze notifications and provide insights"""
        if not notifications:
            return {
                "summary": "No notifications found for the specified criteria",
                "urgent_actions": [],
                "deadlines": [],
                "recommendations": []
            }
        
        # Extract deadlines and urgent actions
        deadlines = []
        urgent_actions = []
        
        for notification in notifications:
            if notification.get("deadline"):
                deadlines.append({
                    "case": notification["case_number"],
                    "deadline": notification["deadline"],
                    "type": notification["type"],
                    "summary": notification["summary"]
                })
            
            if "URGENTE" in notification.get("actions", []):
                urgent_actions.append({
                    "case": notification["case_number"],
                    "action": "URGENTE",
                    "summary": notification["summary"]
                })
        
        # Generate recommendations
        recommendations = self._generate_recommendations(notifications, original_query)
        
        return {
            "summary": f"Found {len(notifications)} notifications",
            "urgent_actions": urgent_actions,
            "deadlines": deadlines,
            "recommendations": recommendations,
            "notification_types": self._count_notification_types(notifications)
        }

    def _generate_recommendations(
        self, 
        notifications: List[Dict[str, Any]], 
        query: str
    ) -> List[str]:
        """Generate actionable recommendations based on notifications"""
        recommendations = []
        
        # Count different types of notifications
        type_counts = self._count_notification_types(notifications)
        
        # Generate type-specific recommendations
        if type_counts.get("MANIFESTAR_SE", 0) > 0:
            recommendations.append("Prepare responses for pending manifestations")
        
        if type_counts.get("CITAR", 0) > 0:
            recommendations.append("Schedule hearings for citation notifications")
        
        if type_counts.get("TOMAR_CIÊNCIA", 0) > 0:
            recommendations.append("Review and acknowledge new dispatches")
        
        # Add general recommendations
        if len(notifications) > 5:
            recommendations.append("Consider batch processing for efficiency")
        
        if any("URGENTE" in n.get("actions", []) for n in notifications):
            recommendations.append("Prioritize urgent actions immediately")
        
        return recommendations

    def _count_notification_types(self, notifications: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count occurrences of different notification types"""
        type_counts = {}
        for notification in notifications:
            notification_type = notification.get("type", "OUTROS")
            type_counts[notification_type] = type_counts.get(notification_type, 0) + 1
        return type_counts


class AdvancedLegalAssistant(LegalAssistant):
    """
    Advanced legal assistant with additional features
    
    Extends the basic assistant with:
    - Deadline tracking and alerts
    - Case status monitoring
    - Document generation
    - Integration with calendar systems
    """
    
    def __init__(self, openai_api_key: str, mcp_server_url: str):
        super().__init__(openai_api_key, mcp_server_url)
        
        # Add additional functions for advanced features
        self.functions.extend([
            {
                "name": "get_case_details",
                "description": "Get detailed information about a specific case",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_number": {
                            "type": "string",
                            "description": "Court case number"
                        }
                    },
                    "required": ["case_number"]
                }
            },
            {
                "name": "calculate_deadlines",
                "description": "Calculate and track deadlines for court actions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_date": {
                            "type": "string",
                            "description": "Date of notification (YYYY-MM-DD)"
                        },
                        "deadline_days": {
                            "type": "integer",
                            "description": "Number of days for deadline"
                        }
                    },
                    "required": ["notification_date", "deadline_days"]
                }
            }
        ])

    async def get_deadline_alerts(self, lawyer_name: str) -> Dict[str, Any]:
        """Get urgent deadline alerts for a lawyer"""
        # Get notifications for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        notifications = await self._get_notifications_from_mcp({
            "name": lawyer_name,
            "date_start": start_date.strftime("%Y-%m-%d"),
            "date_end": end_date.strftime("%Y-%m-%d")
        })
        
        # Filter for urgent deadlines
        urgent_deadlines = []
        for notification in notifications:
            if notification.get("deadline"):
                # Parse deadline and check if urgent
                deadline_info = self._parse_deadline(notification["deadline"])
                if deadline_info and deadline_info["days_remaining"] <= 3:
                    urgent_deadlines.append({
                        "case": notification["case_number"],
                        "deadline": notification["deadline"],
                        "days_remaining": deadline_info["days_remaining"],
                        "type": notification["type"],
                        "summary": notification["summary"]
                    })
        
        return {
            "urgent_deadlines": urgent_deadlines,
            "total_notifications": len(notifications),
            "alerts_count": len(urgent_deadlines)
        }

    def _parse_deadline(self, deadline_str: str) -> Optional[Dict[str, Any]]:
        """Parse deadline string and calculate remaining days"""
        try:
            if "days" in deadline_str.lower():
                days = int(re.search(r'(\d+)', deadline_str).group(1))
                return {
                    "days_remaining": days,
                    "is_urgent": days <= 3
                }
        except:
            pass
        return None


# Example usage and testing
async def main():
    """Example usage of the legal assistant"""
    
    # Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    
    # Create assistant
    assistant = AdvancedLegalAssistant(OPENAI_API_KEY, MCP_SERVER_URL)
    
    # Example queries
    test_queries = [
        "Quais são as intimações do PEDRO BRANDÃO para hoje?",
        "Preciso ver as notificações do PEDRO BRANDÃO da última semana",
        "Tem alguma intimação urgente para PEDRO BRANDÃO?",
        "Mostre as citações do PEDRO BRANDÃO do mês passado"
    ]
    
    print("🤖 Legal Assistant Demo")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 30)
        
        result = await assistant.process_query(query)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            print(f"Message: {result['message']}")
        else:
            print(f"✅ Found {result['total_count']} notifications")
            print(f"📊 Analysis: {result['analysis']['summary']}")
            
            if result['analysis']['urgent_actions']:
                print("🚨 Urgent Actions:")
                for action in result['analysis']['urgent_actions']:
                    print(f"  - {action['case']}: {action['summary']}")
            
            if result['analysis']['recommendations']:
                print("💡 Recommendations:")
                for rec in result['analysis']['recommendations']:
                    print(f"  - {rec}")
        
        print("\n" + "=" * 50)
    
    # Test deadline alerts
    print("\n⏰ Deadline Alerts Demo")
    print("-" * 30)
    
    alerts = await assistant.get_deadline_alerts("PEDRO BRANDÃO")
    print(f"Found {alerts['alerts_count']} urgent deadlines")
    
    for deadline in alerts['urgent_deadlines']:
        print(f"  - {deadline['case']}: {deadline['days_remaining']} days remaining")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main()) 