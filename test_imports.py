#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify all dependencies are installed correctly"""

import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Testing core dependencies...")

try:
    import flask
    print("[OK] Flask")
except ImportError as e:
    print(f"[FAIL] Flask: {e}")

try:
    import groq
    print("[OK] groq")
except ImportError as e:
    print(f"[FAIL] groq: {e}")

try:
    import speech_recognition
    print("[OK] SpeechRecognition")
except ImportError as e:
    print(f"[FAIL] SpeechRecognition: {e}")

try:
    import gtts
    print("[OK] gTTS")
except ImportError as e:
    print(f"[FAIL] gTTS: {e}")

try:
    import pygame
    print("[OK] pygame")
except ImportError as e:
    print(f"[FAIL] pygame: {e}")

try:
    import pyautogui
    print("[OK] pyautogui")
except ImportError as e:
    print(f"[FAIL] pyautogui: {e}")

try:
    import keyboard
    print("[OK] keyboard")
except ImportError as e:
    print(f"[FAIL] keyboard: {e}")

try:
    import selenium
    print("[OK] selenium")
except ImportError as e:
    print(f"[FAIL] selenium: {e}")

try:
    import apscheduler
    print("[OK] APScheduler")
except ImportError as e:
    print(f"[FAIL] APScheduler: {e}")

try:
    from dotenv import load_dotenv
    print("[OK] python-dotenv")
except ImportError as e:
    print(f"[FAIL] python-dotenv: {e}")

try:
    import dateutil
    print("[OK] python-dateutil")
except ImportError as e:
    print(f"[FAIL] python-dateutil: {e}")

print("\nTesting project modules...")

try:
    from groq_agent import GroqAgent
    print("[OK] groq_agent")
except ImportError as e:
    print(f"[FAIL] groq_agent: {e}")

try:
    from voice_module import VoiceModule
    print("[OK] voice_module")
except ImportError as e:
    print(f"[FAIL] voice_module: {e}")

try:
    from memory_module import MemoryModule
    print("[OK] memory_module")
except ImportError as e:
    print(f"[FAIL] memory_module: {e}")

try:
    from automation_module import AutomationModule
    print("[OK] automation_module")
except ImportError as e:
    print(f"[FAIL] automation_module: {e}")

try:
    from scheduler_module import SchedulerModule
    print("[OK] scheduler_module")
except ImportError as e:
    print(f"[FAIL] scheduler_module: {e}")

print("\n[SUCCESS] All tests completed!")

