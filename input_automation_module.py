"""
Input Automation Module
Handles keyboard and mouse automation - typing, clicking, searching, navigation
"""

import logging
import time
from typing import Dict, Optional
import pygetwindow as gw

logger = logging.getLogger(__name__)

# Keyboard and Mouse Automation
try:
    import pyautogui
    import keyboard
    INPUT_AUTOMATION_AVAILABLE = True
    # Safety settings
    pyautogui.PAUSE = 0.1  # Small pause between actions
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
except ImportError:
    INPUT_AUTOMATION_AVAILABLE = False
    logger.warning("pyautogui or keyboard not installed. Input automation will be limited.")

class InputAutomationModule:
    """Handles keyboard and mouse automation like a human"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
    
    def type_text(self, params: Dict) -> str:
        """Type text using keyboard (simulates human typing)"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Keyboard automation not available. Install: pip install pyautogui keyboard"
        
        try:
            text = params.get('text', '')
            speed = params.get('speed', 0.05)  # Seconds per character (human-like)
            press_enter = params.get('press_enter', False)
            
            if not text:
                return "Error: No text provided to type"
            
            # Wait a moment for focus
            time.sleep(0.5)
            
            # Type text character by character (human-like)
            pyautogui.write(text, interval=speed)
            
            if press_enter:
                time.sleep(0.2)
                pyautogui.press('enter')
            
            if self.memory_module:
                self.memory_module.log_activity('keyboard_type', {
                    'text_length': len(text),
                    'pressed_enter': press_enter
                })
            
            return f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}"
        
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return f"Error typing: {e}"
    
    def press_key(self, params: Dict) -> str:
        """Press keyboard key or combination"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Keyboard automation not available"
        
        try:
            key = params.get('key', '')
            keys = params.get('keys', [])  # For combinations like ['ctrl', 'c']
            
            if keys:
                # Press key combination
                pyautogui.hotkey(*keys)
                return f"Pressed key combination: {'+'.join(keys)}"
            elif key:
                pyautogui.press(key.lower())
                return f"Pressed key: {key}"
            else:
                return "Error: No key specified"
        
        except Exception as e:
            logger.error(f"Error pressing key: {e}")
            return f"Error: {e}"
    
    def click_mouse(self, params: Dict) -> str:
        """Click mouse at position or current location"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Mouse automation not available"
        
        try:
            x = params.get('x')
            y = params.get('y')
            button = params.get('button', 'left')  # left, right, middle
            clicks = params.get('clicks', 1)
            double = params.get('double', False)
            
            if x is not None and y is not None:
                # Click at specific position
                if double:
                    pyautogui.doubleClick(x, y, button=button)
                else:
                    pyautogui.click(x, y, clicks=clicks, button=button)
                return f"Clicked at position ({x}, {y}) with {button} button"
            else:
                # Click at current mouse position
                if double:
                    pyautogui.doubleClick(button=button)
                else:
                    pyautogui.click(clicks=clicks, button=button)
                return f"Clicked at current position with {button} button"
        
        except Exception as e:
            logger.error(f"Error clicking mouse: {e}")
            return f"Error: {e}"
    
    def move_mouse(self, params: Dict) -> str:
        """Move mouse to position"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Mouse automation not available"
        
        try:
            x = params.get('x')
            y = params.get('y')
            duration = params.get('duration', 0.5)  # Animation duration
            
            if x is None or y is None:
                return "Error: x and y coordinates required"
            
            pyautogui.moveTo(x, y, duration=duration)
            return f"Moved mouse to ({x}, {y})"
        
        except Exception as e:
            logger.error(f"Error moving mouse: {e}")
            return f"Error: {e}"
    
    def search_in_application(self, params: Dict) -> str:
        """Search in current application using Ctrl+F"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Keyboard automation not available"
        
        try:
            search_text = params.get('text', '')
            if not search_text:
                return "Error: Search text required"
            
            # Press Ctrl+F to open search
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # Type search text
            pyautogui.write(search_text, interval=0.05)
            time.sleep(0.3)
            
            # Press Enter to search (or Escape to close, depending on app)
            # Most apps use Enter to find, some use Escape to close
            # We'll use Enter for now
            pyautogui.press('enter')
            
            return f"Searched for: {search_text}"
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return f"Error: {e}"
    
    def navigate_with_keyboard(self, params: Dict) -> str:
        """Navigate using keyboard shortcuts"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Keyboard automation not available"
        
        try:
            action = params.get('action', '')  # tab, enter, arrow_up, arrow_down, etc.
            modifier = params.get('modifier', '')  # ctrl, alt, shift
            
            if modifier:
                pyautogui.hotkey(modifier, action)
                return f"Navigated: {modifier}+{action}"
            else:
                pyautogui.press(action)
                return f"Navigated: {action}"
        
        except Exception as e:
            logger.error(f"Error navigating: {e}")
            return f"Error: {e}"
    
    def perform_sequence(self, params: Dict) -> str:
        """Perform a sequence of keyboard/mouse actions"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return "Input automation not available"
        
        try:
            actions = params.get('actions', [])  # List of action dictionaries
            
            if not actions:
                return "Error: No actions provided"
            
            results = []
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'type':
                    self.type_text(action.get('params', {}))
                elif action_type == 'click':
                    self.click_mouse(action.get('params', {}))
                elif action_type == 'press':
                    self.press_key(action.get('params', {}))
                elif action_type == 'wait':
                    time.sleep(action.get('duration', 1))
                
                results.append(f"Executed: {action_type}")
            
            return f"Performed {len(actions)} actions: {', '.join(results[:5])}"
        
        except Exception as e:
            logger.error(f"Error performing sequence: {e}")
            return f"Error: {e}"
    
    def get_mouse_position(self) -> Dict:
        """Get current mouse position"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return {'error': 'Mouse automation not available'}
        
        try:
            x, y = pyautogui.position()
            return {'x': x, 'y': y}
        except Exception as e:
            logger.error(f"Error getting mouse position: {e}")
            return {'error': str(e)}
    
    def get_screen_size(self) -> Dict:
        """Get screen size"""
        if not INPUT_AUTOMATION_AVAILABLE:
            return {'error': 'Screen info not available'}
        
        try:
            width, height = pyautogui.size()
            return {'width': width, 'height': height}
        except Exception as e:
            logger.error(f"Error getting screen size: {e}")
            return {'error': str(e)}

