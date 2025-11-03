"""
Scheduler Module - Handles reminders and background jobs
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.date import DateTrigger
    APSCHEDULER_AVAILABLE = True
except ImportError:
    APSCHEDULER_AVAILABLE = False
    logger.warning("apscheduler not installed. Reminders will have limited functionality.")

class SchedulerModule:
    """Manages scheduled tasks and reminders"""
    
    def __init__(self, memory_module, voice_module=None, automation_module=None):
        self.memory_module = memory_module
        self.voice_module = voice_module
        self.automation_module = automation_module
        self.scheduler = None
        
        if APSCHEDULER_AVAILABLE:
            try:
                self.scheduler = BackgroundScheduler()
                self.scheduler.start()
                logger.info("Scheduler started successfully")
                
                # Check for due reminders every minute
                self.scheduler.add_job(
                    self.check_reminders,
                    'interval',
                    minutes=1,
                    id='check_reminders'
                )
            except Exception as e:
                logger.error(f"Error initializing scheduler: {e}")
        else:
            logger.warning("APScheduler not available. Reminders will not work automatically.")
    
    def schedule_reminder(self, reminder_id: int, reminder_text: str, reminder_time: str):
        """
        Schedule a reminder
        
        Args:
            reminder_id: ID of the reminder in database
            reminder_text: Text of the reminder
            reminder_time: ISO format datetime string
        """
        if not self.scheduler:
            logger.warning("Scheduler not available")
            return
        
        try:
            # Parse reminder time (handle various formats)
            try:
                # Try ISO format first
                reminder_dt = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
            except ValueError:
                # Try parsing common datetime formats
                from dateutil import parser
                reminder_dt = parser.parse(reminder_time)
            
            # Schedule job
            self.scheduler.add_job(
                self.trigger_reminder,
                DateTrigger(run_date=reminder_dt),
                args=[reminder_id, reminder_text],
                id=f'reminder_{reminder_id}'
            )
            
            logger.info(f"Scheduled reminder {reminder_id} for {reminder_time}")
        
        except Exception as e:
            logger.error(f"Error scheduling reminder: {e}")
    
    def trigger_reminder(self, reminder_id: int, reminder_text: str):
        """Trigger a reminder"""
        try:
            # Mark as triggered in database
            self.memory_module.mark_reminder_triggered(reminder_id)
            
            # Speak the reminder
            if self.voice_module:
                self.voice_module.speak(f"Reminder: {reminder_text}", language='en')
            
            # Log the reminder
            self.memory_module.log_activity('reminder_triggered', {
                'reminder_id': reminder_id,
                'reminder_text': reminder_text
            })
            
            logger.info(f"Triggered reminder {reminder_id}: {reminder_text}")
        
        except Exception as e:
            logger.error(f"Error triggering reminder: {e}")
    
    def check_reminders(self):
        """Check for due reminders (called periodically)"""
        try:
            reminders = self.memory_module.get_all_reminders(include_triggered=False)
            now = datetime.now()
            
            for reminder in reminders:
                try:
                    # Parse reminder time (handle various formats)
                    try:
                        reminder_time_str = reminder['reminder_time'].replace('Z', '+00:00')
                        reminder_time = datetime.fromisoformat(reminder_time_str)
                        # Make naive if it has timezone info (for comparison with naive datetime)
                        if reminder_time.tzinfo is not None:
                            reminder_time = reminder_time.replace(tzinfo=None)
                    except ValueError:
                        from dateutil import parser
                        reminder_time = parser.parse(reminder['reminder_time'])
                        # Make naive if it has timezone info
                        if reminder_time.tzinfo is not None:
                            reminder_time = reminder_time.replace(tzinfo=None)
                    
                    # Check if reminder is due (within 1 minute tolerance)
                    if reminder_time <= now:
                        reminder_id = reminder['id']
                        reminder_text = reminder['reminder_text']
                        
                        # Trigger the reminder
                        self.trigger_reminder(reminder_id, reminder_text)
                        
                        # Remove from scheduler if it exists
                        try:
                            self.scheduler.remove_job(f'reminder_{reminder_id}')
                        except:
                            pass
                
                except Exception as e:
                    logger.error(f"Error checking reminder {reminder.get('id')}: {e}")
        
        except Exception as e:
            logger.error(f"Error checking reminders: {e}")
    
    def schedule_daily_tasks(self):
        """Schedule recurring daily tasks"""
        if not self.scheduler:
            return
        
        # Example: Morning routine check at 9 AM
        try:
            self.scheduler.add_job(
                self.morning_routine,
                CronTrigger(hour=9, minute=0),
                id='morning_routine'
            )
            logger.info("Scheduled daily morning routine")
        except Exception as e:
            logger.error(f"Error scheduling daily tasks: {e}")
    
    def morning_routine(self):
        """Execute morning routine tasks"""
        try:
            if self.voice_module:
                self.voice_module.speak("Good morning! Here's your daily briefing.", language='en')
            
            # Get today's tasks
            tasks = self.memory_module.get_all_tasks(status='pending')
            task_count = len(tasks)
            
            if self.voice_module:
                if task_count > 0:
                    self.voice_module.speak(f"You have {task_count} pending tasks today.", language='en')
                else:
                    self.voice_module.speak("You have no pending tasks. Great job!", language='en')
            
            # Get upcoming reminders
            reminders = self.memory_module.get_all_reminders(include_triggered=False)
            if reminders:
                reminder_count = len(reminders)
                if self.voice_module:
                    self.voice_module.speak(f"You have {reminder_count} reminders coming up.", language='en')
            
            self.memory_module.log_activity('morning_routine', {
                'tasks_count': task_count,
                'reminders_count': len(reminders)
            })
        
        except Exception as e:
            logger.error(f"Error in morning routine: {e}")
    
    def shutdown(self):
        """Shutdown scheduler"""
        if self.scheduler:
            try:
                self.scheduler.shutdown()
                logger.info("Scheduler shut down")
            except Exception as e:
                logger.error(f"Error shutting down scheduler: {e}")

