"""
AI Desktop Assistant - Main Flask Application
Handles web interface, API endpoints, and orchestration
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import logging
from datetime import datetime
import threading

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path)  # Load from project root directory
except ImportError:
    pass  # python-dotenv not installed, use system env vars
except Exception as e:
    pass  # Will log later after logging is configured

from groq_agent import GroqAgent
from voice_module import VoiceModule
from automation_module import AutomationModule
from memory_module import MemoryModule
from scheduler_module import SchedulerModule
from code_module import CodeModule
from learning_module import LearningModule
from system_module import SystemModule
from file_advanced_module import AdvancedFileModule
from productivity_module import ProductivityModule
from ai_advanced_module import AdvancedAIModule
from communication_module import CommunicationModule
from web_scraping_module import WebScrapingModule
from health_module import HealthModule
from input_automation_module import InputAutomationModule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-assistant-secret-key-2024')
CORS(app)

# Initialize modules
groq_agent = None
voice_module = None
automation_module = None
memory_module = None
scheduler_module = None
code_module = None
learning_module = None
system_module = None
file_advanced_module = None
productivity_module = None
ai_advanced_module = None
communication_module = None
web_scraping_module = None
health_module = None
input_automation_module = None

def initialize_modules():
    """Initialize all assistant modules"""
    global groq_agent, voice_module, automation_module, memory_module, scheduler_module
    global code_module, learning_module, system_module, file_advanced_module, productivity_module
    global ai_advanced_module, communication_module, web_scraping_module, health_module
    global input_automation_module
    
    try:
        # Initialize memory first (needed by other modules)
        memory_module = MemoryModule()
        
        # Initialize Groq agent
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            logger.warning("GROQ_API_KEY not found in environment variables")
        groq_agent = GroqAgent(api_key, memory_module)
        
        # Initialize voice module
        voice_module = VoiceModule()
        
        # Initialize automation module
        automation_module = AutomationModule(memory_module)
        
        # Initialize new modules (before passing to AI module)
        code_module = CodeModule(memory_module)
        learning_module = LearningModule(memory_module)
        system_module = SystemModule(memory_module)
        file_advanced_module = AdvancedFileModule(memory_module)
        productivity_module = ProductivityModule(memory_module)
        communication_module = CommunicationModule(memory_module)
        web_scraping_module = WebScrapingModule(memory_module)
        health_module = HealthModule(memory_module)
        input_automation_module = InputAutomationModule(memory_module)
        
        # Initialize AI module (needs groq_agent which is already initialized above)
        ai_advanced_module = AdvancedAIModule(groq_agent, memory_module)
        
        # Pass new modules to groq_agent and automation_module
        if groq_agent:
            groq_agent.code_module = code_module
            groq_agent.learning_module = learning_module
            groq_agent.system_module = system_module
            groq_agent.file_advanced_module = file_advanced_module
            groq_agent.productivity_module = productivity_module
            groq_agent.ai_advanced_module = ai_advanced_module
            groq_agent.communication_module = communication_module
            groq_agent.web_scraping_module = web_scraping_module
            groq_agent.health_module = health_module
            groq_agent.input_automation_module = input_automation_module
        
        if automation_module:
            automation_module.code_module = code_module
            automation_module.learning_module = learning_module
            automation_module.system_module = system_module
            automation_module.file_advanced_module = file_advanced_module
            automation_module.productivity_module = productivity_module
            automation_module.ai_advanced_module = ai_advanced_module
            automation_module.communication_module = communication_module
            automation_module.web_scraping_module = web_scraping_module
            automation_module.health_module = health_module
            automation_module.input_automation_module = input_automation_module
        
        # Initialize scheduler
        scheduler_module = SchedulerModule(memory_module, voice_module, automation_module)
        
        logger.info("All modules initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing modules: {e}")
        return False

# Initialize on startup
if not initialize_modules():
    logger.error("Failed to initialize modules. Some features may not work.")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages (text or voice transcription)"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        language = data.get('language', 'en')  # 'en' or 'ur'
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Store user message in memory
        memory_module.add_chat_entry('user', user_message, language)
        
        # Get response from Groq agent
        assistant_response, actions = groq_agent.process_query(user_message, language)
        
        # Store assistant response
        memory_module.add_chat_entry('assistant', assistant_response, language)
        
        # Execute any actions if needed
        action_results = []
        if actions:
            for action in actions:
                try:
                    result = automation_module.execute_action(action)
                    action_results.append({
                        'action': action.get('type'),
                        'result': result,
                        'success': True
                    })
                except Exception as e:
                    action_results.append({
                        'action': action.get('type'),
                        'result': str(e),
                        'success': False
                    })
        
        return jsonify({
            'response': assistant_response,
            'actions': action_results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/start', methods=['POST'])
def start_voice_listening():
    """Start continuous voice listening"""
    try:
        if voice_module:
            voice_module.start_listening()
            return jsonify({'status': 'listening_started'})
        return jsonify({'error': 'Voice module not available'}), 500
    except Exception as e:
        logger.error(f"Error starting voice listening: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/stop', methods=['POST'])
def stop_voice_listening():
    """Stop voice listening"""
    try:
        if voice_module:
            voice_module.stop_listening()
            return jsonify({'status': 'listening_stopped'})
        return jsonify({'error': 'Voice module not available'}), 500
    except Exception as e:
        logger.error(f"Error stopping voice listening: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file from frontend"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        
        if voice_module:
            text, detected_lang = voice_module.transcribe_audio(audio_file, language)
            return jsonify({
                'text': text,
                'language': detected_lang
            })
        return jsonify({'error': 'Voice module not available'}), 500
    
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = memory_module.get_all_tasks()
        return jsonify({'tasks': tasks})
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    try:
        data = request.json
        task_text = data.get('task', '')
        due_date = data.get('due_date')
        
        task_id = memory_module.add_task(task_text, due_date)
        return jsonify({'task_id': task_id, 'status': 'added'})
    except Exception as e:
        logger.error(f"Error adding task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task status"""
    try:
        data = request.json
        status = data.get('status', 'pending')
        memory_module.update_task(task_id, status=status)
        return jsonify({'status': 'updated'})
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        memory_module.delete_task(task_id)
        return jsonify({'status': 'deleted'})
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    """Get all reminders"""
    try:
        reminders = memory_module.get_all_reminders()
        return jsonify({'reminders': reminders})
    except Exception as e:
        logger.error(f"Error getting reminders: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reminders', methods=['POST'])
def add_reminder():
    """Add a new reminder"""
    try:
        data = request.json
        reminder_text = data.get('reminder', '')
        reminder_time = data.get('time')
        
        reminder_id = memory_module.add_reminder(reminder_text, reminder_time)
        
        # Schedule the reminder
        if scheduler_module:
            scheduler_module.schedule_reminder(reminder_id, reminder_text, reminder_time)
        
        return jsonify({'reminder_id': reminder_id, 'status': 'added'})
    except Exception as e:
        logger.error(f"Error adding reminder: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get activity logs"""
    try:
        logs = memory_module.get_activity_logs()
        return jsonify({'logs': logs})
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """Convert text to speech with natural voice"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # IMPORTANT: Stop listening to prevent echo/feedback
        if voice_module.is_listening:
            voice_module.stop_listening()
            logger.info("Stopped listening before speaking to prevent echo")
        
        # Speak the text in a separate thread to not block the response
        import threading
        def speak_and_resume():
            try:
                voice_module.speak(text, language)
                # Wait a moment before resuming to ensure audio is done
                import time
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error in speak thread: {e}")
        
        speak_thread = threading.Thread(target=speak_and_resume)
        speak_thread.daemon = True
        speak_thread.start()
        
        return jsonify({'status': 'speaking'})
    except Exception as e:
        logger.error(f"Error in speak: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/memory/query', methods=['POST'])
def query_memory():
    """Query chat history and memory"""
    try:
        data = request.json
        query = data.get('query', '')
        
        results = memory_module.search_chat_history(query)
        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"Error querying memory: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    """Get system information"""
    try:
        if system_module:
            info = system_module.get_system_info()
            return jsonify({'info': info})
        return jsonify({'error': 'System module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/productivity/stats', methods=['GET'])
def get_productivity_stats():
    """Get productivity statistics"""
    try:
        if productivity_module:
            stats = productivity_module.get_productivity_stats()
            return jsonify({'stats': stats})
        return jsonify({'error': 'Productivity module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting productivity stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning/flashcards', methods=['GET'])
def get_flashcards():
    """Get flashcards"""
    try:
        category = request.args.get('category', None)
        if learning_module:
            flashcards = learning_module.get_flashcards(category)
            return jsonify({'flashcards': flashcards})
        return jsonify({'error': 'Learning module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting flashcards: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning/stats', methods=['GET'])
def get_learning_stats():
    """Get learning statistics"""
    try:
        if learning_module:
            stats = learning_module.get_study_stats()
            return jsonify({'stats': stats})
        return jsonify({'error': 'Learning module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting learning stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health/stats', methods=['GET'])
def get_health_stats():
    """Get health statistics"""
    try:
        if health_module:
            stats = health_module.get_health_stats()
            return jsonify({'stats': stats})
        return jsonify({'error': 'Health module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting health stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/input/mouse_position', methods=['GET'])
def get_mouse_position():
    """Get current mouse position"""
    try:
        if input_automation_module:
            position = input_automation_module.get_mouse_position()
            return jsonify({'position': position})
        return jsonify({'error': 'Input automation module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting mouse position: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/input/screen_size', methods=['GET'])
def get_screen_size():
    """Get screen size"""
    try:
        if input_automation_module:
            size = input_automation_module.get_screen_size()
            return jsonify({'size': size})
        return jsonify({'error': 'Input automation module not available'}), 503
    except Exception as e:
        logger.error(f"Error getting screen size: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting AI Desktop Assistant on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)

