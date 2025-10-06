#!/usr/bin/env python3
"""
Quick test to verify OpenAI API key
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("=" * 60)
print("OpenAI API Key Test")
print("=" * 60)
print(f"API Key found: {api_key[:20]}...{api_key[-10:] if api_key else 'NOT FOUND'}")
print()

if not api_key or api_key == "your_openai_api_key_here":
    print("❌ ERROR: API key not set correctly in .env file")
    exit(1)

try:
    print("Testing API key...")
    client = OpenAI(api_key=api_key)
    
    # Try a simple API call
    response = client.models.list()
    print("✅ SUCCESS! API key is valid")
    print(f"Available models: {len(list(response.data))} models found")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print()
    print("This usually means:")
    print("1. Your API key is expired or revoked")
    print("2. You need to get a new API key from: https://platform.openai.com/api-keys")
    print("3. Make sure you have billing enabled on your OpenAI account")
