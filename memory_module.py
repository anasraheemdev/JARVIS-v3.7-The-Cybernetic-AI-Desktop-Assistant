"""
Memory Module - Handles persistent storage using SQLite
Stores chats, tasks, reminders, and activity logs
"""

import sqlite3
import logging
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class MemoryModule:
    """Manages persistent memory using SQLite database"""
    
    def __init__(self, db_path: str = 'assistant_memory.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Chat history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_text TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    due_date DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME
                )
            ''')
            
            # Reminders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reminder_text TEXT NOT NULL,
                    reminder_time DATETIME NOT NULL,
                    triggered BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Activity logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT NOT NULL,
                    details TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def add_chat_entry(self, role: str, content: str, language: str = 'en'):
        """Add a chat entry to history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_history (role, content, language)
                VALUES (?, ?, ?)
            ''', (role, content, language))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding chat entry: {e}")
    
    def get_recent_chats(self, limit: int = 20) -> List[Dict]:
        """Get recent chat history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT role, content, language, timestamp
                FROM chat_history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            chats = []
            for row in rows:
                chats.append({
                    'role': row['role'],
                    'content': row['content'],
                    'language': row['language'],
                    'timestamp': row['timestamp']
                })
            
            conn.close()
            return list(reversed(chats))  # Return in chronological order
        
        except Exception as e:
            logger.error(f"Error getting recent chats: {e}")
            return []
    
    def search_chat_history(self, query: str) -> List[Dict]:
        """Search chat history for a query"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT role, content, language, timestamp
                FROM chat_history
                WHERE content LIKE ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (f'%{query}%',))
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'role': row['role'],
                    'content': row['content'],
                    'language': row['language'],
                    'timestamp': row['timestamp']
                })
            
            conn.close()
            return results
        
        except Exception as e:
            logger.error(f"Error searching chat history: {e}")
            return []
    
    def add_task(self, task_text: str, due_date: Optional[str] = None) -> int:
        """Add a new task"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO tasks (task_text, due_date)
                VALUES (?, ?)
            ''', (task_text, due_date))
            
            task_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.log_activity('add_task', {'task_id': task_id, 'task_text': task_text})
            return task_id
        
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return -1
    
    def get_all_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """Get all tasks, optionally filtered by status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if status:
                cursor.execute('''
                    SELECT id, task_text, status, due_date, created_at, completed_at
                    FROM tasks
                    WHERE status = ?
                    ORDER BY created_at DESC
                ''', (status,))
            else:
                cursor.execute('''
                    SELECT id, task_text, status, due_date, created_at, completed_at
                    FROM tasks
                    ORDER BY created_at DESC
                ''')
            
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append({
                    'id': row['id'],
                    'task_text': row['task_text'],
                    'status': row['status'],
                    'due_date': row['due_date'],
                    'created_at': row['created_at'],
                    'completed_at': row['completed_at']
                })
            
            conn.close()
            return tasks
        
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            return []
    
    def update_task(self, task_id: int, status: Optional[str] = None, task_text: Optional[str] = None):
        """Update a task"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if status:
                updates.append('status = ?')
                params.append(status)
                if status == 'completed':
                    updates.append('completed_at = ?')
                    params.append(datetime.now().isoformat())
            
            if task_text:
                updates.append('task_text = ?')
                params.append(task_text)
            
            if updates:
                params.append(task_id)
                cursor.execute(f'''
                    UPDATE tasks
                    SET {', '.join(updates)}
                    WHERE id = ?
                ''', params)
                
                conn.commit()
                self.log_activity('update_task', {'task_id': task_id, 'status': status})
            
            conn.close()
        
        except Exception as e:
            logger.error(f"Error updating task: {e}")
    
    def delete_task(self, task_id: int):
        """Delete a task"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            
            conn.commit()
            conn.close()
            
            self.log_activity('delete_task', {'task_id': task_id})
        
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
    
    def add_reminder(self, reminder_text: str, reminder_time: str) -> int:
        """Add a new reminder"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO reminders (reminder_text, reminder_time)
                VALUES (?, ?)
            ''', (reminder_text, reminder_time))
            
            reminder_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.log_activity('add_reminder', {
                'reminder_id': reminder_id,
                'reminder_text': reminder_text,
                'reminder_time': reminder_time
            })
            
            return reminder_id
        
        except Exception as e:
            logger.error(f"Error adding reminder: {e}")
            return -1
    
    def get_all_reminders(self, include_triggered: bool = False) -> List[Dict]:
        """Get all reminders"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if include_triggered:
                cursor.execute('''
                    SELECT id, reminder_text, reminder_time, triggered, created_at
                    FROM reminders
                    ORDER BY reminder_time ASC
                ''')
            else:
                cursor.execute('''
                    SELECT id, reminder_text, reminder_time, triggered, created_at
                    FROM reminders
                    WHERE triggered = 0
                    ORDER BY reminder_time ASC
                ''')
            
            rows = cursor.fetchall()
            reminders = []
            for row in rows:
                reminders.append({
                    'id': row['id'],
                    'reminder_text': row['reminder_text'],
                    'reminder_time': row['reminder_time'],
                    'triggered': bool(row['triggered']),
                    'created_at': row['created_at']
                })
            
            conn.close()
            return reminders
        
        except Exception as e:
            logger.error(f"Error getting reminders: {e}")
            return []
    
    def mark_reminder_triggered(self, reminder_id: int):
        """Mark a reminder as triggered"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE reminders
                SET triggered = 1
                WHERE id = ?
            ''', (reminder_id,))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            logger.error(f"Error marking reminder as triggered: {e}")
    
    def log_activity(self, action_type: str, details: Dict):
        """Log an activity"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            details_json = json.dumps(details)
            
            cursor.execute('''
                INSERT INTO activity_logs (action_type, details)
                VALUES (?, ?)
            ''', (action_type, details_json))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            logger.error(f"Error logging activity: {e}")
    
    def get_activity_logs(self, limit: int = 100) -> List[Dict]:
        """Get activity logs"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT action_type, details, timestamp
                FROM activity_logs
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            logs = []
            for row in rows:
                try:
                    details = json.loads(row['details']) if row['details'] else {}
                except:
                    details = {}
                
                logs.append({
                    'action_type': row['action_type'],
                    'details': details,
                    'timestamp': row['timestamp']
                })
            
            conn.close()
            return logs
        
        except Exception as e:
            logger.error(f"Error getting activity logs: {e}")
            return []

