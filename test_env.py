#!/usr/bin/env python
"""Test script to verify .env file loading"""

import os
from dotenv import load_dotenv

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')

print(f"Looking for .env file at: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    print("\n=== File Content ===")
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(repr(content))
        print("\n=== Parsed Lines ===")
        for line in content.split('\n'):
            if line.strip() and not line.strip().startswith('#'):
                print(f"  {line}")

# Load the .env file
load_dotenv(env_path)

# Check if GROQ_API_KEY is loaded
api_key = os.getenv('GROQ_API_KEY')
print(f"\n=== Environment Variables ===")
print(f"GROQ_API_KEY loaded: {api_key is not None}")
if api_key:
    if api_key == 'your_groq_api_key_here':
        print("⚠️  WARNING: API key is still the placeholder!")
        print("   Please edit .env file and replace 'your_groq_api_key_here' with your actual API key")
    else:
        print(f"✅ API key is configured: {api_key[:10]}...{api_key[-4:]}")
else:
    print("❌ GROQ_API_KEY not found in environment")

