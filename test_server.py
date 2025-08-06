#!/usr/bin/env python3
"""
Test script for MCP DJEN Server
Run this to verify the server is working correctly
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_health():
    """Test health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")

async def test_root():
    """Test root endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")

async def test_intimations():
    """Test intimations endpoint"""
    async with httpx.AsyncClient() as client:
        # Test successful request
        params = {
            "name": "PEDRO BRANDÃO",
            "date_start": "2025-08-06",
            "date_end": "2025-08-06"
        }
        response = await client.get(f"{BASE_URL}/intimations", params=params)
        print(f"✅ Intimations endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} notifications")
            for i, notification in enumerate(data[:2]):  # Show first 2
                print(f"   {i+1}. {notification['type']} - {notification['summary'][:50]}...")
        else:
            print(f"   Error: {response.text}")

async def test_case_details():
    """Test case details endpoint"""
    async with httpx.AsyncClient() as client:
        case_number = "1234567-89.2024.8.13.0001"
        response = await client.get(f"{BASE_URL}/intimations/{case_number}")
        print(f"✅ Case details: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Case: {data['case_number']}")
            print(f"   Type: {data['type']}")
        else:
            print(f"   Error: {response.text}")

async def test_courts():
    """Test courts endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/courts")
        print(f"✅ Courts endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Available courts: {len(data)}")
            for court in data:
                print(f"   - {court['code']}: {court['name']}")

async def test_error_handling():
    """Test error handling"""
    async with httpx.AsyncClient() as client:
        # Test invalid date format
        params = {
            "name": "PEDRO BRANDÃO",
            "date_start": "invalid-date",
            "date_end": "2025-08-06"
        }
        response = await client.get(f"{BASE_URL}/intimations", params=params)
        print(f"✅ Error handling (invalid date): {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"   Error: {data.get('message')}")
        else:
            print(f"   Unexpected status: {response.status_code}")

async def test_rate_limiting():
    """Test rate limiting"""
    async with httpx.AsyncClient() as client:
        print("✅ Testing rate limiting...")
        
        # Make multiple requests quickly
        for i in range(5):
            params = {
                "name": "PEDRO BRANDÃO",
                "date_start": "2025-08-06",
                "date_end": "2025-08-06"
            }
            response = await client.get(f"{BASE_URL}/intimations", params=params)
            print(f"   Request {i+1}: {response.status_code}")
            
            if response.status_code == 429:
                print("   Rate limit hit!")
                break

async def main():
    """Run all tests"""
    print("🚀 Testing MCP DJEN Server...")
    print("=" * 50)
    
    try:
        await test_health()
        print()
        
        await test_root()
        print()
        
        await test_intimations()
        print()
        
        await test_case_details()
        print()
        
        await test_courts()
        print()
        
        await test_error_handling()
        print()
        
        await test_rate_limiting()
        print()
        
        print("✅ All tests completed!")
        
    except httpx.ConnectError:
        print("❌ Could not connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 