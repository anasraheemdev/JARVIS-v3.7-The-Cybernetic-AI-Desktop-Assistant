#!/usr/bin/env python
"""Test script to verify Groq model works"""

from dotenv import load_dotenv
import os
from groq_agent import GroqAgent
from memory_module import MemoryModule

# Load environment
load_dotenv()

# Initialize
memory = MemoryModule()
agent = GroqAgent(os.getenv('GROQ_API_KEY'), memory)

if not agent.client:
    print("[FAIL] Groq client not initialized")
    exit(1)

print("[OK] Groq client initialized")
print(f"Testing model: llama-3.3-70b-versatile")

# Test query
try:
    response, actions = agent.process_query("Hello, can you hear me?", "en")
    print(f"[OK] Success! Response: {response[:100]}...")
    print("[OK] Model is working correctly!")
except Exception as e:
    print(f"[FAIL] Error: {e}")

