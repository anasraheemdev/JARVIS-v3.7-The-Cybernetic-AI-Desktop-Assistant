"""
Learning Module
Handles study session tracking, flashcards, note-taking, and research
"""

import os
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import sqlite3

logger = logging.getLogger(__name__)

class LearningModule:
    """Handles learning and study-related operations"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.home_dir = Path(os.path.expanduser('~'))
        self.notes_dir = self.home_dir / 'Documents' / 'JARVIS_Notes'
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize learning database
        self.db_path = Path(__file__).parent / 'learning.db'
        self._init_database()
    
    def _init_database(self):
        """Initialize learning database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Study sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    duration_minutes INTEGER,
                    notes TEXT,
                    date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Flashcards table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    category TEXT,
                    difficulty INTEGER DEFAULT 1,
                    times_studied INTEGER DEFAULT 0,
                    last_studied TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Learning database initialized")
        except Exception as e:
            logger.error(f"Error initializing learning database: {e}")
    
    def start_study_session(self, params: Dict) -> str:
        """Start a study session"""
        try:
            subject = params.get('subject', 'General')
            notes = params.get('notes', '')
            
            # Store session start
            session_data = {
                'subject': subject,
                'start_time': datetime.now().isoformat(),
                'notes': notes
            }
            
            if self.memory_module:
                self.memory_module.log_activity('study_session_start', session_data)
            
            return f"Started study session for: {subject}"
        
        except Exception as e:
            logger.error(f"Error starting study session: {e}")
            return f"Error: {e}"
    
    def end_study_session(self, params: Dict) -> str:
        """End a study session and record duration"""
        try:
            subject = params.get('subject', 'General')
            duration = params.get('duration', 0)  # in minutes
            notes = params.get('notes', '')
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO study_sessions (subject, duration_minutes, notes, date, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (subject, duration, notes, datetime.now().date().isoformat(), datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            if self.memory_module:
                self.memory_module.log_activity('study_session_end', {
                    'subject': subject,
                    'duration_minutes': duration
                })
            
            return f"Recorded study session: {subject} for {duration} minutes"
        
        except Exception as e:
            logger.error(f"Error ending study session: {e}")
            return f"Error: {e}"
    
    def create_flashcard(self, params: Dict) -> str:
        """Create a new flashcard"""
        try:
            front = params.get('front', '')
            back = params.get('back', '')
            category = params.get('category', 'General')
            
            if not front or not back:
                return "Error: Both 'front' and 'back' are required"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO flashcards (front, back, category, created_at)
                VALUES (?, ?, ?, ?)
            """, (front, back, category, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            return f"Created flashcard in category '{category}': {front}"
        
        except Exception as e:
            logger.error(f"Error creating flashcard: {e}")
            return f"Error: {e}"
    
    def get_flashcards(self, category: Optional[str] = None) -> List[Dict]:
        """Get flashcards, optionally filtered by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT id, front, back, category, difficulty, times_studied
                    FROM flashcards
                    WHERE category = ?
                    ORDER BY last_studied ASC, created_at DESC
                """, (category,))
            else:
                cursor.execute("""
                    SELECT id, front, back, category, difficulty, times_studied
                    FROM flashcards
                    ORDER BY last_studied ASC, created_at DESC
                """)
            
            flashcards = []
            for row in cursor.fetchall():
                flashcards.append({
                    'id': row[0],
                    'front': row[1],
                    'back': row[2],
                    'category': row[3],
                    'difficulty': row[4],
                    'times_studied': row[5]
                })
            
            conn.close()
            return flashcards
        
        except Exception as e:
            logger.error(f"Error getting flashcards: {e}")
            return []
    
    def save_note(self, params: Dict) -> str:
        """Save a note to markdown file"""
        try:
            title = params.get('title', f"Note_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            content = params.get('content', '')
            category = params.get('category', 'General')
            
            # Create category folder
            category_dir = self.notes_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Create markdown file
            note_file = category_dir / f"{title}.md"
            with open(note_file, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Category:** {category}\n\n---\n\n")
                f.write(content)
            
            if self.memory_module:
                self.memory_module.log_activity('note_saved', {
                    'title': title,
                    'category': category,
                    'path': str(note_file)
                })
            
            return f"Note saved: {note_file}"
        
        except Exception as e:
            logger.error(f"Error saving note: {e}")
            return f"Error: {e}"
    
    def search_wikipedia(self, params: Dict) -> str:
        """Search Wikipedia (opens in browser)"""
        try:
            query = params.get('query', '')
            if not query:
                return "Error: Search query required"
            
            # URL encode query
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_query}"
            
            # Open in browser
            import webbrowser
            webbrowser.open(url)
            
            return f"Opened Wikipedia search for: {query}"
        
        except Exception as e:
            logger.error(f"Error searching Wikipedia: {e}")
            return f"Error: {e}"
    
    def search_youtube(self, params: Dict) -> str:
        """Search YouTube (opens in browser)"""
        try:
            query = params.get('query', '')
            if not query:
                return "Error: Search query required"
            
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            import webbrowser
            webbrowser.open(url)
            
            return f"Opened YouTube search for: {query}"
        
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            return f"Error: {e}"
    
    def get_study_stats(self) -> Dict:
        """Get study statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total study time
            cursor.execute("SELECT SUM(duration_minutes) FROM study_sessions")
            total_minutes = cursor.fetchone()[0] or 0
            
            # Study sessions count
            cursor.execute("SELECT COUNT(*) FROM study_sessions")
            session_count = cursor.fetchone()[0]
            
            # Flashcard count
            cursor.execute("SELECT COUNT(*) FROM flashcards")
            flashcard_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_study_minutes': total_minutes,
                'total_study_hours': round(total_minutes / 60, 2),
                'session_count': session_count,
                'flashcard_count': flashcard_count
            }
        
        except Exception as e:
            logger.error(f"Error getting study stats: {e}")
            return {}

