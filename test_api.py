#!/usr/bin/env python3
"""
Simple test script to verify the API is working correctly.
This can be run without Firebase configuration to test the basic functionality.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoints():
    """Test the health check endpoints."""
    print("Testing health endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"GET / - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the API server is running on localhost:8000")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"GET /health - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    return True

def test_report_request():
    """Test the report request endpoint."""
    print("Testing report request endpoint...")
    
    # Sample request data
    test_data = {
        "reportId": f"test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "userId": "test-user-123",
        "businessInfo": {
            "businessName": "Test Company Inc.",
            "postalCode": "90210",
            "country": "United States",
            "industry": "Technology"
        },
        "finalPrompt": "Generate a comprehensive market analysis report for a technology startup focusing on competitive landscape, target demographics, and growth opportunities in the US market."
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/request-report",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        print(f"POST /api/request-report - Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Report request successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
        
        print()
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Report request failed: {e}")
        return False

def test_api_documentation():
    """Test that API documentation is accessible."""
    print("Testing API documentation endpoints...")
    
    # Test Swagger UI
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"GET /docs (Swagger UI) - Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Swagger UI is accessible")
        else:
            print("❌ Swagger UI not accessible")
    except requests.exceptions.RequestException as e:
        print(f"❌ Swagger UI test failed: {e}")
    
    # Test ReDoc
    try:
        response = requests.get(f"{BASE_URL}/redoc")
        print(f"GET /redoc (ReDoc) - Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ ReDoc is accessible")
        else:
            print("❌ ReDoc not accessible")
    except requests.exceptions.RequestException as e:
        print(f"❌ ReDoc test failed: {e}")
    
    print()

def main():
    """Run all tests."""
    print("🚀 Starting API Tests")
    print("=" * 50)
    
    # Test health endpoints
    if not test_health_endpoints():
        print("❌ Health check tests failed. Exiting.")
        return
    
    # Test API documentation
    test_api_documentation()
    
    # Test report request
    test_report_request()
    
    print("=" * 50)
    print("✅ All tests completed!")
    print("\nNext steps:")
    print("1. Configure Firebase credentials in .env file")
    print("2. Test with real Firebase integration")
    print("3. Replace dummy_report_processor with actual AI integration")

if __name__ == "__main__":
    main()
