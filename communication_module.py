"""
Communication Module
Handles Telegram, LinkedIn, contact management, and social media
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional, List
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

class CommunicationModule:
    """Handles advanced communication features"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.db_path = Path(__file__).parent / 'communication.db'
        self._init_database()
    
    def _init_database(self):
        """Initialize communication database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Contacts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    whatsapp TEXT,
                    telegram TEXT,
                    notes TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            
            # LinkedIn drafts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS linkedin_drafts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT NOT NULL,
                    scheduled_time TEXT,
                    posted BOOLEAN DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Communication database initialized")
        except Exception as e:
            logger.error(f"Error initializing communication database: {e}")
    
    def add_contact(self, params: Dict) -> str:
        """Add a contact to the database"""
        try:
            name = params.get('name', '')
            email = params.get('email', '')
            phone = params.get('phone', '')
            whatsapp = params.get('whatsapp', '')
            telegram = params.get('telegram', '')
            notes = params.get('notes', '')
            
            if not name:
                return "Error: Contact name required"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contacts (name, email, phone, whatsapp, telegram, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, whatsapp, telegram, notes, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            return f"Added contact: {name}"
        
        except Exception as e:
            logger.error(f"Error adding contact: {e}")
            return f"Error: {e}"
    
    def get_contact(self, params: Dict) -> str:
        """Get contact information"""
        try:
            name = params.get('name', '')
            
            if not name:
                return "Error: Contact name required"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, email, phone, whatsapp, telegram, notes
                FROM contacts
                WHERE name LIKE ?
            """, (f'%{name}%',))
            
            contact = cursor.fetchone()
            conn.close()
            
            if contact:
                return f"Contact: {contact[0]}\nEmail: {contact[1] or 'N/A'}\nPhone: {contact[2] or 'N/A'}\nWhatsApp: {contact[3] or 'N/A'}\nTelegram: {contact[4] or 'N/A'}\nNotes: {contact[5] or 'N/A'}"
            else:
                return f"Contact not found: {name}"
        
        except Exception as e:
            logger.error(f"Error getting contact: {e}")
            return f"Error: {e}"
    
    def save_linkedin_draft(self, params: Dict) -> str:
        """Save a LinkedIn post draft"""
        try:
            title = params.get('title', '')
            content = params.get('content', '')
            scheduled_time = params.get('scheduled_time', '')
            
            if not content:
                return "Error: Post content required"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO linkedin_drafts (title, content, scheduled_time, created_at)
                VALUES (?, ?, ?, ?)
            """, (title, content, scheduled_time, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            return f"Saved LinkedIn draft: {title or 'Untitled'}"
        
        except Exception as e:
            logger.error(f"Error saving LinkedIn draft: {e}")
            return f"Error: {e}"
    
    def get_linkedin_drafts(self) -> List[Dict]:
        """Get all LinkedIn drafts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, content, scheduled_time, posted, created_at
                FROM linkedin_drafts
                WHERE posted = 0
                ORDER BY created_at DESC
            """)
            
            drafts = []
            for row in cursor.fetchall():
                drafts.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'scheduled_time': row[3],
                    'posted': row[4],
                    'created_at': row[5]
                })
            
            conn.close()
            return drafts
        
        except Exception as e:
            logger.error(f"Error getting LinkedIn drafts: {e}")
            return []

