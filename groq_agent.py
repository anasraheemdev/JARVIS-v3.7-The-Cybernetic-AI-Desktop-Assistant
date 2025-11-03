"""
Groq Agent Module - Handles LLM reasoning and response generation
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

try:
    from groq import Groq
except ImportError:
    Groq = None
    logging.warning("groq package not installed. Install with: pip install groq")

logger = logging.getLogger(__name__)

class GroqAgent:
    """Handles communication with Groq API for AI reasoning"""
    
    def __init__(self, api_key: Optional[str] = None, memory_module=None):
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        self.memory_module = memory_module
        self.client = None
        
        if self.api_key and Groq:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        else:
            logger.warning("Groq API key not provided or package not installed")
    
    def get_system_prompt(self) -> str:
        """Generate system prompt for the assistant"""
        # Get user context from memory
        user_context = ""
        if self.memory_module:
            try:
                # Try to get user profile from database
                import sqlite3
                conn = sqlite3.connect(self.memory_module.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT details FROM activity_logs WHERE action_type = 'user_profile' ORDER BY timestamp DESC LIMIT 1")
                result = cursor.fetchone()
                if result:
                    user_context = f"\n\n**User Context:**\n{result[0]}\n"
                conn.close()
            except:
                pass
        
        return f"""You are JARVIS, an AI Desktop Assistant helping Anas Raheem (AI student & developer). You have access to his full profile and preferences.
{user_context}
**Your Capabilities:**

1. File & Folder Operations:
   - CREATE folders (desktop, documents, downloads, custom paths)
   - ORGANIZE files (sort by type, clean old files)
   - SEARCH file content (find text in files)
   - FIND duplicate files
   - BATCH rename files
   - COMPRESS images
   - MERGE PDFs

2. Applications & Web:
   - OPEN apps and files
   - BROWSE URLs and SEARCH Google, Wikipedia, YouTube
   - OPEN VS Code with files/folders

3. Code Development:
   - CREATE files with code/content
   - CREATE project templates (Flask, React, Python)
   - GIT operations (commit, push, pull, status)
   - RUN terminal commands (with safety checks)
   - GENERATE code snippets

4. Task Management:
   - CREATE reminders and tasks
   - MANAGE to-do lists
   - SET scheduled events

5. Learning & Research:
   - TRACK study sessions
   - CREATE and review flashcards
   - SAVE notes to markdown files
   - SEARCH Wikipedia and YouTube
   - GENERATE study summaries

6. Communication:
   - SEND emails (with confirmation)
   - SEND WhatsApp messages (real-time automation)
   - OPEN WhatsApp and message contacts automatically

7. System Monitoring:
   - GET system info (CPU, RAM, Disk usage)
   - TAKE screenshots
   - MANAGE clipboard (copy/paste)
   - CLEANUP temp files

8. Productivity:
   - START/COMPLETE Pomodoro timers
   - CREATE and TRACK habits
   - GENERATE productivity reports

9. Advanced AI Features:
   - SUMMARIZE documents and text
   - TRANSLATE between languages
   - ANALYZE sentiment of text
   - GENERATE code from descriptions
   - DEBUG code and fix errors

10. Communication Management:
   - MANAGE contacts (email, phone, WhatsApp, Telegram)
   - SAVE LinkedIn post drafts
   - ORGANIZE contact information

11. Web Scraping & Data:
   - SCRAPE websites and extract data
   - EXPORT data to Excel/CSV
   - MONITOR prices (placeholder)

12. Health & Wellness:
   - TRACK water intake
   - LOG exercise activities
   - MONITOR health statistics

13. Keyboard & Mouse Automation:
   - TYPE text naturally (human-like typing speed)
   - PRESS keys and key combinations (Ctrl+C, Alt+Tab, etc.)
   - CLICK mouse at positions or current location
   - MOVE mouse smoothly to coordinates
   - SEARCH in any application (Ctrl+F)
   - NAVIGATE using keyboard shortcuts
   - PERFORM complex sequences of actions

14. Information & Conversation:
   - ANSWER questions
   - REMEMBER past conversations
   - SPEAK in English (default) or Urdu (when requested)

**Action Response Format:**

When user requests an action, respond in JSON:
```json
{{
  "response": "Your natural, friendly response",
  "actions": [
    {{
      "type": "organize_files",
      "parameters": {{
        "action": "create_folder",
        "folder_name": "FolderName",
        "location": "desktop"
      }}
    }}
  ]
}}
```

**Available Action Types:**
- File Operations: `organize_files`, `search_file_content`, `find_duplicates`, `batch_rename`, `compress_image`, `merge_pdfs`
- Applications: `open_app`, `open_vscode`, `browse_url`, `search_google`, `search_wikipedia`, `search_youtube`
- Code Development: `create_file`, `create_project`, `git_operation`, `run_command`
- Learning: `start_study_session`, `end_study_session`, `create_flashcard`, `save_note`
- System: `get_system_info`, `take_screenshot`, `copy_clipboard`
- Productivity: `start_pomodoro`, `complete_pomodoro`, `create_habit`, `complete_habit`
- Advanced AI: `summarize_document`, `translate_text`, `analyze_sentiment`, `generate_code`, `debug_code`
- Communication: `send_email`, `send_whatsapp`, `add_contact`, `get_contact`, `save_linkedin_draft`
- Web Scraping: `scrape_website`, `extract_to_excel`
- Health: `log_water`, `log_exercise`
- Keyboard & Mouse: `type_text`, `press_key`, `click_mouse`, `move_mouse`, `search_in_app`, `navigate_keyboard`, `perform_sequence`
- Tasks: `set_reminder`, `create_task`

**Important:**
- For "create a folder named X" → use organize_files with action="create_folder", folder_name="X", location="desktop"
- For "send WhatsApp to John" → use send_whatsapp with contact="John", message="Your message"
- For "open VS Code" → use open_vscode with optional path parameter
- For "start a 25-minute Pomodoro" → use start_pomodoro with duration=25, task="Work"
- For "create a Flask project" → use create_project with type="flask", name="project_name"
- For "search files for 'hello'" → use search_file_content with text="hello", directory="path"
- For "type 'Hello World'" → use type_text with text="Hello World"
- For "click at position 100, 200" → use click_mouse with x=100, y=200
- For "search for 'test' in current app" → use search_in_app with text="test"
- For "press Ctrl+C" → use press_key with keys=["ctrl", "c"]
- Be proactive and autonomous
- Remember Anas's preferences (tech stack, projects, goals)
- **ALWAYS respond in ENGLISH by default** (only use Urdu if explicitly requested)
- For sensitive operations (delete, format, etc.), ask confirmation first"""

    def process_query(self, user_message: str, language: str = 'en') -> tuple:
        """
        Process user query and return response with actions
        
        Returns:
            tuple: (response_text, actions_list)
        """
        if not self.client:
            return "I'm sorry, the Groq API is not configured. Please set GROQ_API_KEY environment variable.", []
        
        try:
            # Get chat history for context
            chat_history = []
            if self.memory_module:
                recent_chats = self.memory_module.get_recent_chats(limit=10)
                for chat in recent_chats:
                    role = chat.get('role', 'user')
                    content = chat.get('content', '')
                    chat_history.append({
                        'role': role,
                        'content': content
                    })
            
            # Build messages
            messages = [
                {'role': 'system', 'content': self.get_system_prompt()}
            ]
            
            # Add recent chat history (last 10 messages for context)
            messages.extend(chat_history[-10:])
            
            # Add language instruction
            language_instruction = ""
            if language == 'ur':
                language_instruction = " [RESPOND IN URDU]"
            else:
                language_instruction = " [RESPOND IN ENGLISH]"
            
            # Add current user message with language instruction
            messages.append({
                'role': 'user',
                'content': user_message + language_instruction
            })
            
            # Get response from Groq
            # Using llama-3.3-70b-versatile (replacement for deprecated llama-3.1-70b-versatile)
            # Alternative models: "llama-3.1-8b-instant" (faster), "mixtral-8x7b-32768" (fast)
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Current supported model
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                response_format={"type": "json_object"} if self._should_use_json(user_message) else None
            )
            
            assistant_message = response.choices[0].message.content
            
            # Parse response and extract actions
            actions = self._extract_actions(assistant_message, user_message)
            response_text = self._extract_response_text(assistant_message)
            
            # Log the interaction
            if self.memory_module:
                self.memory_module.log_activity('groq_query', {
                    'user_message': user_message,
                    'response': response_text,
                    'actions': actions
                })
            
            return response_text, actions
        
        except Exception as e:
            logger.error(f"Error processing query with Groq: {e}")
            return f"I encountered an error: {str(e)}", []
    
    def _should_use_json(self, user_message: str) -> bool:
        """Determine if the response should be in JSON format (for action requests)"""
        action_keywords = [
            'open', 'run', 'launch', 'search', 'browse', 'send', 'email',
            'delete', 'move', 'copy', 'organize', 'clean', 'remind',
            'handle', 'perform', 'execute', 'do', 'make', 'create',
            'folder', 'file', 'task', 'reminder', 'schedule'
        ]
        return any(keyword in user_message.lower() for keyword in action_keywords)
    
    def _extract_actions(self, assistant_message: str, user_message: str) -> List[Dict]:
        """Extract action commands from assistant response"""
        actions = []
        
        try:
            # Try to parse as JSON first
            if assistant_message.strip().startswith('{'):
                data = json.loads(assistant_message)
                if 'actions' in data:
                    actions.extend(data['actions'])
                return actions
        except json.JSONDecodeError:
            pass
        
        # Extract actions from natural language using keyword matching
        message_lower = user_message.lower()
        
        # Open application
        if any(x in message_lower for x in ['open', 'launch', 'run', 'start']):
            if 'google' in message_lower or 'browser' in message_lower or 'chrome' in message_lower:
                actions.append({
                    'type': 'browse_url',
                    'parameters': {'url': 'https://www.google.com'}
                })
            elif 'search' in message_lower and 'google' in message_lower:
                # Extract search query
                search_query = self._extract_search_query(user_message)
                if search_query:
                    actions.append({
                        'type': 'search_google',
                        'parameters': {'query': search_query}
                    })
        
        # Search Google
        if 'search' in message_lower and 'google' in message_lower:
            search_query = self._extract_search_query(user_message)
            if search_query:
                actions.append({
                    'type': 'search_google',
                    'parameters': {'query': search_query}
                })
        
        # Send email
        if any(x in message_lower for x in ['send email', 'email', 'mail to']):
            email_info = self._extract_email_info(user_message)
            if email_info:
                actions.append({
                    'type': 'send_email',
                    'parameters': email_info
                })
        
        # File operations
        if 'clean' in message_lower and ('download' in message_lower or 'downloads' in message_lower):
            actions.append({
                'type': 'organize_files',
                'parameters': {'directory': 'downloads', 'action': 'clean'}
            })
        
        # Reminder
        if 'remind' in message_lower or 'reminder' in message_lower:
            reminder_info = self._extract_reminder_info(user_message)
            if reminder_info:
                actions.append({
                    'type': 'set_reminder',
                    'parameters': reminder_info
                })
        
        return actions
    
    def _extract_response_text(self, assistant_message: str) -> str:
        """Extract readable response text from assistant message"""
        try:
            if assistant_message.strip().startswith('{'):
                data = json.loads(assistant_message)
                return data.get('response', assistant_message)
        except json.JSONDecodeError:
            pass
        return assistant_message
    
    def _extract_search_query(self, message: str) -> Optional[str]:
        """Extract search query from user message"""
        keywords = ['search', 'for', 'find', 'look up']
        message_lower = message.lower()
        
        for keyword in keywords:
            if keyword in message_lower:
                idx = message_lower.find(keyword)
                # Try to extract text after keyword
                parts = message[idx:].split()
                if len(parts) > 1:
                    # Remove common words and join
                    query_parts = [p for p in parts[1:] if p not in ['on', 'in', 'google', 'the', 'for']]
                    return ' '.join(query_parts)
        
        # If no keyword found, return message after "search" or similar
        return None
    
    def _extract_email_info(self, message: str) -> Optional[Dict]:
        """Extract email information from user message"""
        # Simple extraction - can be improved with NLP
        # For now, return None to trigger manual confirmation
        return None
    
    def _extract_reminder_info(self, message: str) -> Optional[Dict]:
        """Extract reminder information from user message"""
        # Simple extraction - can be improved with NLP
        # Example: "remind me to call Ali at 6PM"
        message_lower = message.lower()
        
        if 'remind' in message_lower:
            # Extract time (simplified)
            # In production, use proper NLP/date parsing
            return {
                'text': message,
                'time': None  # Should be parsed from message
            }
        return None

