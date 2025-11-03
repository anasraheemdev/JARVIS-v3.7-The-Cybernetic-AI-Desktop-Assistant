"""
Automation Module - Handles desktop automation tasks
File operations, app launching, browser automation, email sending
"""

import os
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Browser automation
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("selenium not installed. Browser automation will be limited.")

# Desktop control
try:
    import pyautogui
    import keyboard
    PYAG_AVAILABLE = True
except ImportError:
    PYAG_AVAILABLE = False
    logger.warning("pyautogui/keyboard not installed. Desktop control will be limited.")

# Email
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

class AutomationModule:
    """Handles desktop automation and system operations"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.browser = None
        # Fix for Windows usernames with spaces
        import os
        self.home_dir = Path(os.path.expanduser('~'))
        
        # Safety settings for pyautogui
        if PYAG_AVAILABLE:
            pyautogui.PAUSE = 0.5
            pyautogui.FAILSAFE = True
    
    def execute_action(self, action: Dict) -> str:
        """
        Execute an automation action
        
        Args:
            action: Action dictionary with 'type' and 'parameters'
        
        Returns:
            str: Result message
        """
        action_type = action.get('type')
        params = action.get('parameters', {})
        
        try:
            if action_type == 'open_app':
                return self.open_application(params.get('app_name'))
            
            elif action_type == 'browse_url':
                return self.browse_url(params.get('url'))
            
            elif action_type == 'search_google':
                return self.search_google(params.get('query'))
            
            elif action_type == 'send_email':
                return self.send_email(params)
            
            elif action_type == 'send_whatsapp':
                return self.send_whatsapp_message(params)
            
            elif action_type == 'organize_files':
                return self.organize_files(params)
            
            elif action_type == 'set_reminder':
                return self.set_reminder(params)
            
            # Code Development Actions
            elif action_type == 'open_vscode':
                if hasattr(self, 'code_module') and self.code_module:
                    return self.code_module.open_vscode(params.get('path'))
                return "Code module not available"
            
            elif action_type == 'create_file':
                if hasattr(self, 'code_module') and self.code_module:
                    return self.code_module.create_file(
                        params.get('path', ''),
                        params.get('content', ''),
                        params.get('language', 'text')
                    )
                return "Code module not available"
            
            elif action_type == 'git_operation':
                if hasattr(self, 'code_module') and self.code_module:
                    return self.code_module.git_operation(params)
                return "Code module not available"
            
            elif action_type == 'create_project':
                if hasattr(self, 'code_module') and self.code_module:
                    return self.code_module.create_project_template(params)
                return "Code module not available"
            
            elif action_type == 'run_command':
                if hasattr(self, 'code_module') and self.code_module:
                    return self.code_module.run_terminal_command(params)
                return "Code module not available"
            
            # Learning Actions
            elif action_type == 'start_study_session':
                if hasattr(self, 'learning_module') and self.learning_module:
                    return self.learning_module.start_study_session(params)
                return "Learning module not available"
            
            elif action_type == 'end_study_session':
                if hasattr(self, 'learning_module') and self.learning_module:
                    return self.learning_module.end_study_session(params)
                return "Learning module not available"
            
            elif action_type == 'create_flashcard':
                if hasattr(self, 'learning_module') and self.learning_module:
                    return self.learning_module.create_flashcard(params)
                return "Learning module not available"
            
            elif action_type == 'save_note':
                if hasattr(self, 'learning_module') and self.learning_module:
                    return self.learning_module.save_note(params)
                return "Learning module not available"
            
            elif action_type == 'search_wikipedia':
                if hasattr(self, 'learning_module') and self.learning_module:
                    return self.learning_module.search_wikipedia(params)
                return "Learning module not available"
            
            elif action_type == 'search_youtube':
                if hasattr(self, 'learning_module') and self.learning_module:
                    return self.learning_module.search_youtube(params)
                return "Learning module not available"
            
            # System Actions
            elif action_type == 'get_system_info':
                if hasattr(self, 'system_module') and self.system_module:
                    info = self.system_module.get_system_info()
                    return f"System Info:\nCPU: {info.get('cpu_percent', 0)}%\nMemory: {info.get('memory', {}).get('percent', 0)}%\nDisk: {info.get('disk', {}).get('percent', 0)}%"
                return "System module not available"
            
            elif action_type == 'take_screenshot':
                if hasattr(self, 'system_module') and self.system_module:
                    return self.system_module.take_screenshot(params.get('filename'))
                return "System module not available"
            
            elif action_type == 'copy_clipboard':
                if hasattr(self, 'system_module') and self.system_module:
                    return self.system_module.copy_to_clipboard(params.get('text', ''))
                return "System module not available"
            
            # Advanced File Actions
            elif action_type == 'search_file_content':
                if hasattr(self, 'file_advanced_module') and self.file_advanced_module:
                    return self.file_advanced_module.search_file_content(params)
                return "File module not available"
            
            elif action_type == 'find_duplicates':
                if hasattr(self, 'file_advanced_module') and self.file_advanced_module:
                    return self.file_advanced_module.find_duplicate_files(params)
                return "File module not available"
            
            elif action_type == 'batch_rename':
                if hasattr(self, 'file_advanced_module') and self.file_advanced_module:
                    return self.file_advanced_module.batch_rename_files(params)
                return "File module not available"
            
            elif action_type == 'compress_image':
                if hasattr(self, 'file_advanced_module') and self.file_advanced_module:
                    return self.file_advanced_module.compress_image(params)
                return "File module not available"
            
            elif action_type == 'merge_pdfs':
                if hasattr(self, 'file_advanced_module') and self.file_advanced_module:
                    return self.file_advanced_module.merge_pdfs(params)
                return "File module not available"
            
            # Productivity Actions
            elif action_type == 'start_pomodoro':
                if hasattr(self, 'productivity_module') and self.productivity_module:
                    return self.productivity_module.start_pomodoro(params)
                return "Productivity module not available"
            
            elif action_type == 'complete_pomodoro':
                if hasattr(self, 'productivity_module') and self.productivity_module:
                    return self.productivity_module.complete_pomodoro()
                return "Productivity module not available"
            
            elif action_type == 'create_habit':
                if hasattr(self, 'productivity_module') and self.productivity_module:
                    return self.productivity_module.create_habit(params)
                return "Productivity module not available"
            
            elif action_type == 'complete_habit':
                if hasattr(self, 'productivity_module') and self.productivity_module:
                    return self.productivity_module.complete_habit(params)
                return "Productivity module not available"
            
            # Advanced AI Actions
            elif action_type == 'summarize_document':
                if hasattr(self, 'ai_advanced_module') and self.ai_advanced_module:
                    return self.ai_advanced_module.summarize_document(params)
                return "AI module not available"
            
            elif action_type == 'translate_text':
                if hasattr(self, 'ai_advanced_module') and self.ai_advanced_module:
                    return self.ai_advanced_module.translate_text(params)
                return "AI module not available"
            
            elif action_type == 'analyze_sentiment':
                if hasattr(self, 'ai_advanced_module') and self.ai_advanced_module:
                    return self.ai_advanced_module.analyze_sentiment(params)
                return "AI module not available"
            
            elif action_type == 'generate_code':
                if hasattr(self, 'ai_advanced_module') and self.ai_advanced_module:
                    return self.ai_advanced_module.generate_code(params)
                return "AI module not available"
            
            elif action_type == 'debug_code':
                if hasattr(self, 'ai_advanced_module') and self.ai_advanced_module:
                    return self.ai_advanced_module.debug_code(params)
                return "AI module not available"
            
            # Communication Actions
            elif action_type == 'add_contact':
                if hasattr(self, 'communication_module') and self.communication_module:
                    return self.communication_module.add_contact(params)
                return "Communication module not available"
            
            elif action_type == 'get_contact':
                if hasattr(self, 'communication_module') and self.communication_module:
                    return self.communication_module.get_contact(params)
                return "Communication module not available"
            
            elif action_type == 'save_linkedin_draft':
                if hasattr(self, 'communication_module') and self.communication_module:
                    return self.communication_module.save_linkedin_draft(params)
                return "Communication module not available"
            
            # Web Scraping Actions
            elif action_type == 'scrape_website':
                if hasattr(self, 'web_scraping_module') and self.web_scraping_module:
                    return self.web_scraping_module.scrape_website(params)
                return "Web scraping module not available"
            
            elif action_type == 'extract_to_excel':
                if hasattr(self, 'web_scraping_module') and self.web_scraping_module:
                    return self.web_scraping_module.extract_to_excel(params)
                return "Web scraping module not available"
            
            # Health Actions
            elif action_type == 'log_water':
                if hasattr(self, 'health_module') and self.health_module:
                    return self.health_module.log_water_intake(params)
                return "Health module not available"
            
            elif action_type == 'log_exercise':
                if hasattr(self, 'health_module') and self.health_module:
                    return self.health_module.log_exercise(params)
                return "Health module not available"
            
            # Input Automation Actions (Keyboard & Mouse)
            elif action_type == 'type_text':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.type_text(params)
                return "Input automation module not available"
            
            elif action_type == 'press_key':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.press_key(params)
                return "Input automation module not available"
            
            elif action_type == 'click_mouse':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.click_mouse(params)
                return "Input automation module not available"
            
            elif action_type == 'move_mouse':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.move_mouse(params)
                return "Input automation module not available"
            
            elif action_type == 'search_in_app':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.search_in_application(params)
                return "Input automation module not available"
            
            elif action_type == 'navigate_keyboard':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.navigate_with_keyboard(params)
                return "Input automation module not available"
            
            elif action_type == 'perform_sequence':
                if hasattr(self, 'input_automation_module') and self.input_automation_module:
                    return self.input_automation_module.perform_sequence(params)
                return "Input automation module not available"
            
            else:
                return f"Unknown action type: {action_type}"
        
        except Exception as e:
            logger.error(f"Error executing action {action_type}: {e}")
            return f"Error: {str(e)}"
    
    def open_application(self, app_name: str) -> str:
        """Open an application by name"""
        try:
            # Map common app names to commands
            app_commands = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'browser': 'chrome.exe',
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'explorer': 'explorer.exe',
                'command': 'cmd.exe',
                'powershell': 'powershell.exe',
            }
            
            command = app_commands.get(app_name.lower(), app_name)
            
            # Try to launch
            subprocess.Popen(command, shell=True)
            
            self._log_action('open_app', {'app': app_name})
            return f"Opened {app_name}"
        
        except Exception as e:
            logger.error(f"Error opening app {app_name}: {e}")
            return f"Could not open {app_name}: {str(e)}"
    
    def browse_url(self, url: str) -> str:
        """Open URL in browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Try using default browser
            if os.name == 'nt':  # Windows
                os.startfile(url)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.Popen(['xdg-open', url])
            
            self._log_action('browse_url', {'url': url})
            return f"Opened {url}"
        
        except Exception as e:
            logger.error(f"Error browsing URL {url}: {e}")
            return f"Could not open {url}: {str(e)}"
    
    def search_google(self, query: str) -> str:
        """Search Google for a query"""
        try:
            import urllib.parse
            search_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/search?q={search_query}"
            return self.browse_url(search_url)
        
        except Exception as e:
            logger.error(f"Error searching Google: {e}")
            return f"Could not search Google: {str(e)}"
    
    def organize_files(self, params: Dict) -> str:
        """Organize files in a directory or create folders"""
        try:
            action = params.get('action', 'organize')
            
            # Handle folder creation
            if action == 'create_folder':
                folder_name = params.get('folder_name', 'NewFolder')
                location = params.get('location', 'desktop').lower()
                
                # Determine the base path
                if location == 'desktop':
                    base_path = self.home_dir / 'Desktop'
                elif location == 'documents':
                    base_path = self.home_dir / 'Documents'
                elif location == 'downloads':
                    base_path = self.home_dir / 'Downloads'
                else:
                    # Custom path
                    base_path = Path(location)
                
                # Create the folder
                folder_path = base_path / folder_name
                folder_path.mkdir(parents=True, exist_ok=True)
                
                self._log_action('create_folder', {
                    'folder': str(folder_path),
                    'name': folder_name,
                    'location': location
                })
                
                return f"Created folder '{folder_name}' at {location} ({folder_path})"
            
            # Handle other file organization actions
            directory = params.get('directory', 'downloads')
            
            # Get directory path
            if directory.lower() == 'downloads':
                target_path = self.home_dir / 'Downloads'
            else:
                target_path = Path(directory)
            
            if not target_path.exists():
                return f"Directory not found: {target_path}"
            
            if action == 'clean':
                return self._clean_downloads(target_path)
            elif action == 'organize':
                return self._organize_downloads(target_path)
            else:
                return f"Unknown organization action: {action}"
        
        except Exception as e:
            logger.error(f"Error organizing files: {e}")
            return f"Error organizing files: {str(e)}"
    
    def _clean_downloads(self, downloads_path: Path) -> str:
        """Clean old files from downloads folder"""
        try:
            if not downloads_path.exists():
                return f"Downloads folder not found: {downloads_path}"
            
            deleted_count = 0
            total_size = 0
            
            for file_path in downloads_path.iterdir():
                if file_path.is_file():
                    # Delete files older than 30 days or ask user
                    file_size = file_path.stat().st_size
                    total_size += file_size
                    deleted_count += 1
            
            # In production, implement actual deletion with user confirmation
            self._log_action('clean_files', {
                'directory': str(downloads_path),
                'files_count': deleted_count
            })
            
            return f"Found {deleted_count} files in downloads folder"
        
        except Exception as e:
            logger.error(f"Error cleaning downloads: {e}")
            return f"Error: {str(e)}"
    
    def _organize_downloads(self, downloads_path: Path) -> str:
        """Organize downloads into folders by file type"""
        try:
            if not downloads_path.exists():
                return f"Downloads folder not found: {downloads_path}"
            
            organized = 0
            
            for file_path in downloads_path.iterdir():
                if file_path.is_file():
                    # Get file extension
                    ext = file_path.suffix.lower() or '.other'
                    folder_name = ext[1:] if ext.startswith('.') else ext
                    
                    # Create folder
                    target_folder = downloads_path / folder_name
                    target_folder.mkdir(exist_ok=True)
                    
                    # Move file
                    target_path = target_folder / file_path.name
                    if not target_path.exists():
                        shutil.move(str(file_path), str(target_path))
                        organized += 1
            
            self._log_action('organize_files', {
                'directory': str(downloads_path),
                'organized': organized
            })
            
            return f"Organized {organized} files"
        
        except Exception as e:
            logger.error(f"Error organizing downloads: {e}")
            return f"Error: {str(e)}"
    
    def send_email(self, params: Dict) -> str:
        """Send an email"""
        try:
            if not EMAIL_AVAILABLE:
                return "Email functionality not available"
            
            # Get email credentials from environment
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            email_address = os.environ.get('EMAIL_ADDRESS')
            email_password = os.environ.get('EMAIL_PASSWORD')
            
            if not email_address or not email_password:
                return "Email credentials not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables."
            
            to_email = params.get('to')
            subject = params.get('subject', 'Message from AI Assistant')
            body = params.get('body', '')
            
            if not to_email:
                return "Recipient email address required"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.send_message(msg)
            
            self._log_action('send_email', {
                'to': to_email,
                'subject': subject
            })
            
            return f"Email sent to {to_email}"
        
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return f"Could not send email: {str(e)}"
    
    def set_reminder(self, params: Dict) -> str:
        """Set a reminder (delegates to memory module)"""
        try:
            if self.memory_module:
                reminder_text = params.get('text', '')
                reminder_time = params.get('time')
                
                reminder_id = self.memory_module.add_reminder(reminder_text, reminder_time)
                return f"Reminder set: {reminder_text}"
            else:
                return "Memory module not available"
        
        except Exception as e:
            logger.error(f"Error setting reminder: {e}")
            return f"Error: {str(e)}"
    
    def send_whatsapp_message(self, params: Dict) -> str:
        """Send a WhatsApp message using WhatsApp Desktop with real-time automation"""
        if not PYAG_AVAILABLE:
            return "Desktop automation not available. Please install pyautogui and keyboard packages."
        
        try:
            contact_name = params.get('contact')
            message = params.get('message')
            
            if not contact_name or not message:
                return "Error: Contact name and message are required."
            
            logger.info(f"Attempting to send WhatsApp message to {contact_name}")
            
            import time
            
            # Step 1: Try to open/focus WhatsApp Desktop
            whatsapp_path = Path(self.home_dir) / "AppData" / "Local" / "WhatsApp" / "WhatsApp.exe"
            
            try:
                # Check if WhatsApp is running
                import psutil
                whatsapp_running = False
                for proc in psutil.process_iter(['name']):
                    try:
                        if 'WhatsApp.exe' in proc.info['name']:
                            whatsapp_running = True
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                if not whatsapp_running:
                    if whatsapp_path.exists():
                        subprocess.Popen([str(whatsapp_path)])
                        logger.info("WhatsApp Desktop launched, waiting for it to load...")
                        time.sleep(8)  # Wait for WhatsApp to fully load
                    else:
                        return "WhatsApp Desktop not found. Please install it from Microsoft Store or whatsapp.com"
                else:
                    logger.info("WhatsApp Desktop is already running")
                    time.sleep(1)
            except ImportError:
                logger.warning("psutil not available, trying to launch WhatsApp anyway")
                if whatsapp_path.exists():
                    subprocess.Popen([str(whatsapp_path)])
                    time.sleep(8)
            except Exception as e:
                logger.warning(f"Could not check/launch WhatsApp: {e}")
            
            # Step 2: Focus on WhatsApp window
            try:
                import pygetwindow as gw
                time.sleep(1)
                whatsapp_windows = gw.getWindowsWithTitle('WhatsApp')
                if whatsapp_windows:
                    whatsapp_windows[0].activate()
                    time.sleep(1)
                    logger.info("WhatsApp window focused")
                else:
                    logger.warning("WhatsApp window not found by title, proceeding anyway")
            except ImportError:
                logger.warning("pygetwindow not available, trying to proceed")
            except Exception as e:
                logger.warning(f"Could not focus WhatsApp window: {e}")
            
            # Step 3: Open search (Ctrl+F) and search for contact
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'f')  # Open search
            time.sleep(1)
            
            # Clear any existing search text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('backspace')
            time.sleep(0.5)
            
            # Step 4: Type contact name (character by character for better compatibility)
            for char in contact_name:
                pyautogui.write(char, interval=0.1)
            time.sleep(2)  # Wait for search results
            
            # Step 5: Press Down arrow and Enter to select first result
            pyautogui.press('down')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(1.5)
            
            # Step 6: Type message (handle special characters and newlines)
            lines = message.split('\n')
            for i, line in enumerate(lines):
                for char in line:
                    pyautogui.write(char, interval=0.03)
                if i < len(lines) - 1:  # Add newline if not last line
                    pyautogui.hotkey('shift', 'enter')
            time.sleep(0.5)
            
            # Step 7: Send message (Enter)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            self._log_action('send_whatsapp', {
                'contact': contact_name,
                'message': message
            })
            
            logger.info(f"✅ WhatsApp message sent to {contact_name}")
            return f"✅ WhatsApp message successfully sent to {contact_name}"
        
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return f"Failed to send WhatsApp message: {str(e)}"
    
    def _log_action(self, action_type: str, details: Dict):
        """Log an action to memory module"""
        if self.memory_module:
            self.memory_module.log_activity(action_type, details)
    
    def close_browser(self):
        """Close browser if open"""
        if self.browser:
            try:
                self.browser.quit()
                self.browser = None
            except:
                pass

