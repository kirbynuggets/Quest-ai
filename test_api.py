#!/usr/bin/env python3
"""
Simple test script for Quest-ai DeepSeek API
"""
import os
from dotenv import load_dotenv
from deepseek_api import DeepSeekAPI

def test_api():
    """Test the DeepSeek API connection"""
    print("Testing DeepSeek API...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"✅ API key loaded: {api_key[:10]}...")
    
    # Create API instance
    api = DeepSeekAPI(api_key)
    
    # Test simple message
    print("Sending test message...")
    response = api.send_message("Hello! Can you tell me what 2+2 equals?")
    
    if response and not response.startswith("Error:"):
        print("✅ API test successful!")
        print(f"Response: {response[:100]}...")
        return True
    else:
        print(f"❌ API test failed: {response}")
        return False

if __name__ == "__main__":
    test_api()
