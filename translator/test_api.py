#!/usr/bin/env python3

from src.api_client import AnthropicClient

def test_api():
    try:
        client = AnthropicClient()
        response = client.send_message("Hello! Please respond with 'API test successful' to confirm the connection works.")
        print("✅ API Connection Successful!")
        print(f"Model: {client.model}")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print("❌ API Connection Failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_api()