"""
System Monitoring Module
Handles system information, screenshots, clipboard, and system cleanup
"""

import os
import logging
import subprocess
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import platform

logger = logging.getLogger(__name__)

# System monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil not installed. System monitoring will be limited.")

# Clipboard
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    logger.warning("pyperclip not installed. Clipboard operations will be limited.")

# Screenshot
try:
    from PIL import ImageGrab
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False
    logger.warning("PIL not available. Screenshots will be limited.")

class SystemModule:
    """Handles system monitoring and operations"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.home_dir = Path(os.path.expanduser('~'))
        self.screenshots_dir = self.home_dir / 'Desktop' / 'Screenshots'
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    def get_system_info(self) -> Dict:
        """Get system information (CPU, RAM, Disk)"""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil not installed"}
        
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_total_gb = round(memory.total / (1024**3), 2)
            memory_available_gb = round(memory.available / (1024**3), 2)
            memory_used_gb = round(memory.used / (1024**3), 2)
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_total_gb = round(disk.total / (1024**3), 2)
            disk_used_gb = round(disk.used / (1024**3), 2)
            disk_free_gb = round(disk.free / (1024**3), 2)
            disk_percent = round((disk.used / disk.total) * 100, 2)
            
            # Platform info
            system_info = {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'memory': {
                    'total_gb': memory_total_gb,
                    'used_gb': memory_used_gb,
                    'available_gb': memory_available_gb,
                    'percent': memory_percent
                },
                'disk': {
                    'total_gb': disk_total_gb,
                    'used_gb': disk_used_gb,
                    'free_gb': disk_free_gb,
                    'percent': disk_percent
                }
            }
            
            return system_info
        
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
    
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """Take a screenshot"""
        if not SCREENSHOT_AVAILABLE:
            return "Screenshot not available. Install Pillow: pip install Pillow"
        
        try:
            if not filename:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot_path = self.screenshots_dir / filename
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            
            if self.memory_module:
                self.memory_module.log_activity('screenshot', {
                    'path': str(screenshot_path)
                })
            
            return f"Screenshot saved: {screenshot_path}"
        
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return f"Error: {e}"
    
    def copy_to_clipboard(self, text: str) -> str:
        """Copy text to clipboard"""
        if not CLIPBOARD_AVAILABLE:
            return "Clipboard not available. Install pyperclip: pip install pyperclip"
        
        try:
            pyperclip.copy(text)
            return f"Copied to clipboard: {text[:50]}..."
        except Exception as e:
            logger.error(f"Error copying to clipboard: {e}")
            return f"Error: {e}"
    
    def get_clipboard(self) -> str:
        """Get text from clipboard"""
        if not CLIPBOARD_AVAILABLE:
            return ""
        
        try:
            return pyperclip.paste()
        except Exception as e:
            logger.error(f"Error getting clipboard: {e}")
            return ""
    
    def cleanup_temp_files(self) -> str:
        """Clean up temporary files"""
        try:
            cleaned_count = 0
            cleaned_size = 0
            
            # Windows temp directories
            temp_dirs = [
                os.path.join(os.environ.get('TEMP', ''), '*'),
                os.path.join(os.environ.get('TMP', ''), '*'),
                str(self.home_dir / 'AppData' / 'Local' / 'Temp')
            ]
            
            # Note: Actual cleanup would require more sophisticated logic
            # This is a placeholder that logs the action
            
            if self.memory_module:
                self.memory_module.log_activity('system_cleanup', {
                    'files_cleaned': cleaned_count,
                    'size_freed_mb': round(cleaned_size / (1024**2), 2)
                })
            
            return f"Cleanup completed. (This is a placeholder - implement actual cleanup logic)"
        
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return f"Error: {e}"
    
    def test_network_speed(self) -> str:
        """Test network speed (opens speedtest.net)"""
        try:
            import webbrowser
            webbrowser.open("https://www.speedtest.net")
            return "Opened speedtest.net for network speed test"
        except Exception as e:
            logger.error(f"Error opening speed test: {e}")
            return f"Error: {e}"

