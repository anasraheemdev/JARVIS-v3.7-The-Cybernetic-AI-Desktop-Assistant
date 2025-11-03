"""
Productivity Module
Handles Pomodoro timer, focus mode, habit tracking, and productivity reports
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class ProductivityModule:
    """Handles productivity and time management features"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.db_path = Path(__file__).parent / 'productivity.db'
        self.active_pomodoro = None
        self._init_database()
    
    def _init_database(self):
        """Initialize productivity database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Pomodoro sessions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pomodoros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    duration_minutes INTEGER DEFAULT 25,
                    task TEXT,
                    completed BOOLEAN DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Habits
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    frequency TEXT DEFAULT 'daily',
                    streak_days INTEGER DEFAULT 0,
                    last_completed TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Productivity database initialized")
        except Exception as e:
            logger.error(f"Error initializing productivity database: {e}")
    
    def start_pomodoro(self, params: Dict) -> str:
        """Start a Pomodoro timer"""
        try:
            duration = params.get('duration', 25)  # minutes
            task = params.get('task', 'Work')
            
            self.active_pomodoro = {
                'start_time': datetime.now(),
                'duration_minutes': duration,
                'task': task
            }
            
            if self.memory_module:
                self.memory_module.log_activity('pomodoro_start', {
                    'duration': duration,
                    'task': task
                })
            
            return f"Started {duration}-minute Pomodoro for: {task}"
        
        except Exception as e:
            logger.error(f"Error starting Pomodoro: {e}")
            return f"Error: {e}"
    
    def complete_pomodoro(self) -> str:
        """Complete the active Pomodoro"""
        try:
            if not self.active_pomodoro:
                return "No active Pomodoro session"
            
            duration = self.active_pomodoro['duration_minutes']
            task = self.active_pomodoro['task']
            
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pomodoros (duration_minutes, task, completed, created_at)
                VALUES (?, ?, 1, ?)
            """, (duration, task, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            self.active_pomodoro = None
            
            if self.memory_module:
                self.memory_module.log_activity('pomodoro_complete', {
                    'duration': duration,
                    'task': task
                })
            
            return f"Pomodoro completed! Great work on: {task}"
        
        except Exception as e:
            logger.error(f"Error completing Pomodoro: {e}")
            return f"Error: {e}"
    
    def create_habit(self, params: Dict) -> str:
        """Create a new habit to track"""
        try:
            name = params.get('name', '')
            frequency = params.get('frequency', 'daily')
            
            if not name:
                return "Error: Habit name required"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO habits (name, frequency, created_at)
                VALUES (?, ?, ?)
            """, (name, frequency, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            return f"Created habit: {name} ({frequency})"
        
        except Exception as e:
            logger.error(f"Error creating habit: {e}")
            return f"Error: {e}"
    
    def complete_habit(self, params: Dict) -> str:
        """Mark a habit as completed"""
        try:
            habit_name = params.get('name', '')
            
            if not habit_name:
                return "Error: Habit name required"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get habit
            cursor.execute("SELECT id, streak_days, last_completed FROM habits WHERE name = ?", (habit_name,))
            habit = cursor.fetchone()
            
            if not habit:
                return f"Habit not found: {habit_name}"
            
            habit_id, current_streak, last_completed = habit
            today = datetime.now().date().isoformat()
            
            # Update streak
            if last_completed == today:
                return f"Habit '{habit_name}' already completed today!"
            elif last_completed:
                last_date = datetime.fromisoformat(last_completed).date()
                yesterday = (datetime.now() - timedelta(days=1)).date()
                if last_date == yesterday:
                    new_streak = current_streak + 1
                else:
                    new_streak = 1
            else:
                new_streak = 1
            
            cursor.execute("""
                UPDATE habits
                SET streak_days = ?, last_completed = ?
                WHERE id = ?
            """, (new_streak, today, habit_id))
            conn.commit()
            conn.close()
            
            return f"Habit completed: {habit_name}! Current streak: {new_streak} days"
        
        except Exception as e:
            logger.error(f"Error completing habit: {e}")
            return f"Error: {e}"
    
    def get_productivity_stats(self) -> Dict:
        """Get productivity statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Pomodoros today
            today = datetime.now().date().isoformat()
            cursor.execute("""
                SELECT COUNT(*), SUM(duration_minutes)
                FROM pomodoros
                WHERE DATE(created_at) = ? AND completed = 1
            """, (today,))
            pomodoro_result = cursor.fetchone()
            pomodoros_today = pomodoro_result[0] or 0
            minutes_today = pomodoro_result[1] or 0
            
            # Habits
            cursor.execute("SELECT COUNT(*), SUM(streak_days) FROM habits")
            habit_result = cursor.fetchone()
            total_habits = habit_result[0] or 0
            total_streak_days = habit_result[1] or 0
            
            conn.close()
            
            return {
                'pomodoros_today': pomodoros_today,
                'focus_minutes_today': minutes_today,
                'total_habits': total_habits,
                'total_streak_days': total_streak_days
            }
        
        except Exception as e:
            logger.error(f"Error getting productivity stats: {e}")
            return {}

