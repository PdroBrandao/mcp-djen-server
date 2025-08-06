#!/usr/bin/env python3
"""
Example: Using MCP DJEN Server with OpenAI Function Calling
This demonstrates how LLMs can interact with the court notifications API
"""

import openai
import json
import httpx
from typing import List, Dict, Any

# Configure OpenAI (replace with your API key)
openai.api_key = "your-openai-api-key"

# MCP Server base URL
MCP_SERVER_URL = "http://localhost:8000"

def get_court_notifications(lawyer_name: str, date_start: str, date_end: str) -> List[Dict[str, Any]]:
    """
    Function to get court notifications from MCP Server
    This is what the LLM will call
    """
    try:
        async def fetch_notifications():
            async with httpx.AsyncClient() as client:
                params = {
                    "name": lawyer_name,
                    "date_start": date_start,
                    "date_end": date_end
                }
                response = await client.get(f"{MCP_SERVER_URL}/intimations", params=params)
                return response.json()
        
        # For simplicity, we'll use a synchronous version
        import asyncio
        return asyncio.run(fetch_notifications())
    
    except Exception as e:
        return {"error": f"Failed to fetch notifications: {str(e)}"}

def setup_function_calling():
    """Define the function schema for OpenAI"""
    return [{
        "name": "get_court_notifications",
        "description": "Get court notifications for a lawyer from the Brazilian DJEN system",
        "parameters": {
            "type": "object",
            "properties": {
                "lawyer_name": {
                    "type": "string",
                    "description": "Full name of the lawyer (e.g., 'ALFREDO RAMOS')"
                },
                "date_start": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format (e.g., '2025-08-06')"
                },
                "date_end": {
                    "type": "string", 
                    "description": "End date in YYYY-MM-DD format (e.g., '2025-08-06')"
                }
            },
            "required": ["lawyer_name", "date_start", "date_end"]
        }
    }]

def process_llm_response(response):
    """Process the LLM response and execute function calls"""
    if response.choices[0].message.function_call:
        function_call = response.choices[0].message.function_call
        
        # Parse function arguments
        args = json.loads(function_call.arguments)
        
        # Execute the function
        if function_call.name == "get_court_notifications":
            result = get_court_notifications(
                lawyer_name=args["lawyer_name"],
                date_start=args["date_start"],
                date_end=args["date_end"]
            )
            
            # Send result back to LLM
            messages = [
                {"role": "user", "content": "What are Alfredo Ramos's court notifications for today?"},
                {"role": "function", "name": "get_court_notifications", "content": json.dumps(result)}
            ]
            
            # Get final response from LLM
            final_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )
            
            return final_response.choices[0].message.content
    
    return response.choices[0].message.content

def example_conversation():
    """Example conversation with the LLM"""
    
    # User query
    user_query = "What are Pedro Brandão's court notifications for today?"
    
    print("🤖 User:", user_query)
    print("-" * 50)
    
    # First LLM call to determine function call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_query}],
        functions=setup_function_calling(),
        function_call="auto",
        temperature=0.7
    )
    
    # Process the response
    result = process_llm_response(response)
    
    print("🤖 Assistant:", result)
    print("-" * 50)

def example_with_claude():
    """Example using Anthropic Claude (if you have access)"""
    
    # This would be the Claude equivalent
    # Note: You'd need the Anthropic SDK installed
    """
    import anthropic
    
    client = anthropic.Anthropic(api_key="your-anthropic-key")
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": "Get court notifications for Alfredo Ramos today"
        }],
        tools=[{
            "name": "get_court_notifications",
            "description": "Get court notifications for a lawyer",
            "input_schema": {
                "type": "object",
                "properties": {
                    "lawyer_name": {"type": "string"},
                    "date_start": {"type": "string"},
                    "date_end": {"type": "string"}
                },
                "required": ["lawyer_name", "date_start", "date_end"]
            }
        }]
    )
    """

def test_mcp_server_directly():
    """Test the MCP server directly without LLM"""
    print("🧪 Testing MCP Server directly...")
    
    try:
        import asyncio
        
        async def test():
            async with httpx.AsyncClient() as client:
                params = {
                    "name": "PEDRO BRANDÃO",
                    "date_start": "2025-08-06",
                    "date_end": "2025-08-06"
                }
                response = await client.get(f"{MCP_SERVER_URL}/intimations", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Found {len(data)} notifications:")
                    for i, notification in enumerate(data):
                        print(f"   {i+1}. {notification['type']} - {notification['summary']}")
                else:
                    print(f"❌ Error: {response.status_code} - {response.text}")
        
        asyncio.run(test())
        
    except Exception as e:
        print(f"❌ Error testing server: {e}")

if __name__ == "__main__":
    print("🚀 MCP DJEN Server - LLM Integration Example")
    print("=" * 60)
    
    # Test server directly first
    test_mcp_server_directly()
    print()
    
    # Example conversation (requires OpenAI API key)
    print("💡 To test with OpenAI, set your API key and uncomment the example_conversation() call")
    # example_conversation()
    
    print("\n📚 This demonstrates how LLMs can interact with court data!")
    print("   The MCP server provides a standardized interface for legal automation.") 