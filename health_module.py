"""
Health & Wellness Module
Handles break reminders, eye strain alerts, water intake tracking, and exercise reminders
"""

import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class HealthModule:
    """Handles health and wellness tracking"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.db_path = Path(__file__).parent / 'health.db'
        self._init_database()
    
    def _init_database(self):
        """Initialize health database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Water intake
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS water_intake (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount_ml INTEGER,
                    date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Exercise log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exercise (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT NOT NULL,
                    duration_minutes INTEGER,
                    date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Health database initialized")
        except Exception as e:
            logger.error(f"Error initializing health database: {e}")
    
    def log_water_intake(self, params: Dict) -> str:
        """Log water intake"""
        try:
            amount = params.get('amount', 250)  # ml
            date = params.get('date', datetime.now().date().isoformat())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO water_intake (amount_ml, date, created_at)
                VALUES (?, ?, ?)
            """, (amount, date, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            # Calculate daily total
            daily_total = self._get_daily_water(date)
            target = 2000  # ml per day
            
            return f"Logged {amount}ml water intake. Daily total: {daily_total}ml / {target}ml"
        
        except Exception as e:
            logger.error(f"Error logging water intake: {e}")
            return f"Error: {e}"
    
    def _get_daily_water(self, date: str) -> int:
        """Get daily water intake total"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(amount_ml) FROM water_intake WHERE date = ?
            """, (date,))
            result = cursor.fetchone()
            conn.close()
            return result[0] or 0
        except:
            return 0
    
    def log_exercise(self, params: Dict) -> str:
        """Log exercise activity"""
        try:
            activity = params.get('activity', 'Exercise')
            duration = params.get('duration', 30)  # minutes
            date = params.get('date', datetime.now().date().isoformat())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exercise (activity, duration_minutes, date, created_at)
                VALUES (?, ?, ?, ?)
            """, (activity, duration, date, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            return f"Logged {duration} minutes of {activity}"
        
        except Exception as e:
            logger.error(f"Error logging exercise: {e}")
            return f"Error: {e}"
    
    def get_health_stats(self) -> Dict:
        """Get health statistics"""
        try:
            today = datetime.now().date().isoformat()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Daily water
            cursor.execute("SELECT SUM(amount_ml) FROM water_intake WHERE date = ?", (today,))
            daily_water = cursor.fetchone()[0] or 0
            
            # Weekly exercise minutes
            week_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
            cursor.execute("""
                SELECT SUM(duration_minutes) FROM exercise WHERE date >= ?
            """, (week_ago,))
            weekly_exercise = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'daily_water_ml': daily_water,
                'daily_water_liters': round(daily_water / 1000, 2),
                'weekly_exercise_minutes': weekly_exercise,
                'weekly_exercise_hours': round(weekly_exercise / 60, 2)
            }
        
        except Exception as e:
            logger.error(f"Error getting health stats: {e}")
            return {}

