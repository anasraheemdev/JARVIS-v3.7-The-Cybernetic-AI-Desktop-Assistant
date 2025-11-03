<div align="center">

# 🤖 JARVIS - AI Desktop Assistant

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

![JARVIS Logo](https://img.shields.io/badge/JARVIS-v3.7-00ffff?style=for-the-badge&logo=artificial-intelligence&logoColor=white)

**A powerful, autonomous AI Desktop Assistant** powered by Groq Cloud API, featuring voice control, desktop automation, persistent memory, and a futuristic cybernetic web interface.

Built with ❤️ using Python, Flask, and modern web technologies.

[🚀 Quick Start](#-installation) • [📖 Features](#-features) • [💻 Usage](#-usage) • [🔧 Configuration](#-configuration)

---

</div>

---

## ✨ Features

<div align="center">

### 🎯 **Core Capabilities**

| 🎤 **Voice Control** | 🧠 **AI Intelligence** |
|---|---|
| Multi-language Support (EN/UR) | Groq Cloud LLM (Llama 3.3 70B) |
| Natural Speech (Google TTS) | Persistent Memory |
| Voice Recognition | User Profile |
| Echo Prevention | Autonomous Actions |

| 🔄 **Automation** | 💻 **Code Development** |
|---|---|
| Application Control | VS Code Integration |
| Keyboard & Mouse Control | Git Operations |
| File Management | Project Templates |
| Browser Automation | Code Generation |
| WhatsApp Automation | Terminal Commands |

</div>

---

### 📚 **Learning & Research**
- **Study Tracking**: Log study sessions with duration
- **Flashcards**: Create and review flashcards by category
- **Note-Taking**: Save notes as Markdown files
- **Research Tools**: Search Wikipedia and YouTube
- **Learning Statistics**: Track progress over time

### 📊 **System Monitoring**
- **Real-time Metrics**: CPU, RAM, Disk usage
- **Screenshots**: Capture screen with one command
- **Clipboard Management**: Copy and paste text
- **Network Monitoring**: Track bandwidth and connection
- **System Cleanup**: Remove temporary files

### ⏰ **Productivity Tools**
- **Pomodoro Timer**: Built-in timer with UI panel
- **Habit Tracking**: Create and track daily habits
- **Task Management**: Create, organize, and complete tasks
- **Smart Reminders**: Automated reminders with voice notifications
- **Productivity Reports**: Track your efficiency

### 🎨 **Advanced AI Features**
- **Document Summarization**: Summarize long texts
- **Translation**: Multi-language translation
- **Sentiment Analysis**: Analyze text emotion
- **Code Debugging**: Find and fix code errors
- **Content Generation**: AI-powered content creation

### 📧 **Communication**
- **Email**: Send emails with confirmation
- **WhatsApp**: Automate WhatsApp Desktop messaging
- **Contact Management**: Store and manage contacts
- **LinkedIn Drafts**: Save post drafts

### 🌐 **Web Scraping**
- **Website Scraping**: Extract data from websites
- **Data Export**: Export to Excel/CSV formats
- **Price Monitoring**: Track product prices (placeholder)

### 💪 **Health & Wellness**
- **Water Intake**: Track daily water consumption (UI panel)
- **Exercise Logging**: Log workouts and activities (UI panel)
- **Health Statistics**: Monitor wellness metrics

### ⌨️ **Keyboard & Mouse Automation**
- **Human-like Typing**: Natural typing speed and rhythm
- **Keyboard Shortcuts**: Press keys and combinations (Ctrl+C, Alt+Tab)
- **Mouse Control**: Click, double-click, right-click
- **Navigation**: Move mouse smoothly to coordinates
- **Search in Apps**: Automatic Ctrl+F with text input
- **Complex Sequences**: Perform multi-step automation workflows

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13+, Flask
- **AI**: Groq Cloud API (Llama 3.3 70B Versatile)
- **Voice**: 
  - SpeechRecognition (STT)
  - Google Cloud Text-to-Speech (Primary TTS)
  - pyttsx3 (Fallback TTS)
  - gTTS (Last Resort)
- **Automation**: 
  - PyAutoGUI (Keyboard/Mouse)
  - Selenium (Browser automation)
  - pygetwindow (Window management)
- **Database**: SQLite3
- **Scheduling**: APScheduler
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **UI**: Custom Cybernetic Interface Design

---

## 📦 Installation

### Prerequisites

- **Python 3.13+** (or 3.11+)
- **pip** (Python package manager)
- **Microphone** (for voice input)
- **Groq API Key** ([Get one here](https://console.groq.com/))
- **Chrome/Chromium** (for browser automation, optional)

### Quick Setup

1. **Clone or download the repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file** in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your_secret_key_here
   
   # Optional: Google Cloud TTS (for ultra-natural voice)
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   
   # Optional: Email configuration
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser**:
   ```
   http://127.0.0.1:5000
   ```

---

## 🚀 Usage

<div align="center">

### **Quick Command Reference**

| 🎯 **Category** | 📝 **Example Command** |
|---|---|
| 🗂️ **Files** | `"Create a folder named Projects"` |
| 🌐 **Web** | `"Search Google for Python tutorials"` |
| 💻 **Code** | `"Create a Flask project named my-api"` |
| 📚 **Learning** | `"Start a study session for Machine Learning"` |
| ⏰ **Productivity** | `"Start a 25-minute Pomodoro"` |
| 💪 **Health** | `"Log 250ml water intake"` |
| 📧 **Communication** | `"Send WhatsApp message to John"` |
| ⌨️ **Automation** | `"Type 'Hello World'"` |

</div>

### Starting the Assistant

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000` (local) and `http://192.168.1.6:5000` (network).

### Voice Commands

1. Click **"▶ ACTIVATE VOICE"** button
2. Speak your command (English or Urdu)
3. JARVIS will process and respond with voice

### Text Commands

1. Type in the chat input field
2. Press **Enter** or click **"EXECUTE"**
3. JARVIS responds and executes actions

### Example Commands

#### File & Folder Operations
```
"Create a folder named Projects on my desktop"
"Search all Python files for 'import flask'"
"Find duplicate files in Downloads"
"Compress image.jpg"
"Merge these PDF files"
```

#### Applications & Web
```
"Open VS Code"
"Open Chrome"
"Search Google for Python tutorials"
"Search YouTube for machine learning"
"Open wikipedia.org"
```

#### Code Development
```
"Create a Flask project named my-api"
"Git commit with message 'Added new features'"
"Open VS Code in my-project folder"
"Generate Python code to sort a list"
"Debug this code: [paste code]"
```

#### Learning & Research
```
"Start a study session for Machine Learning"
"I studied Python for 45 minutes"
"Create a flashcard: front='What is AI?', back='Artificial Intelligence'"
"Save a note titled 'Project Ideas'"
"Search Wikipedia for neural networks"
```

#### System & Productivity
```
"Show me system information"
"Take a screenshot"
"Copy 'Hello World' to clipboard"
"Start a 25-minute Pomodoro"
"Create a habit called 'Exercise daily'"
```

#### Health & Wellness
```
"Log 250ml water intake"
"Log 30 minutes of running"
```

#### Communication
```
"Send email to professor about assignment"
"Send WhatsApp message to John: 'Hello!'"
"Add contact: name=Ali, email=ali@example.com"
```

#### Keyboard & Mouse Automation
```
"Type 'Hello World'"
"Press Ctrl+C"
"Click at position 500, 300"
"Search for 'import' in this application"
"Move mouse to 800, 600"
```

#### Advanced AI
```
"Summarize this text: [paste text]"
"Translate 'Hello' to Urdu"
"Analyze sentiment of this message: [text]"
```

---

## 📁 Project Structure

```
AI Desktop Assistant/
│
├── app.py                          # Main Flask application
├── groq_agent.py                  # Groq API integration & AI reasoning
├── voice_module.py                # Speech-to-Text & Text-to-Speech
├── automation_module.py           # Desktop automation (apps, browser, email)
├── memory_module.py               # SQLite database management
├── scheduler_module.py            # Reminders & background jobs
├── code_module.py                 # Code development tools
├── learning_module.py             # Study tracking & flashcards
├── system_module.py               # System monitoring
├── file_advanced_module.py        # Advanced file operations
├── productivity_module.py         # Pomodoro & habits
├── ai_advanced_module.py          # AI features (summarization, translation)
├── communication_module.py        # Contact management
├── web_scraping_module.py         # Web scraping & data extraction
├── health_module.py               # Health tracking
├── input_automation_module.py     # Keyboard & mouse automation
│
├── templates/
│   └── index.html                 # Cybernetic UI dashboard
│
├── static/
│   ├── css/
│   │   └── style.css             # Custom cybernetic styling
│   └── js/
│       └── app.js                # Frontend JavaScript
│
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (create this)
├── README.md                     # This file
├── QUICKSTART.md                 # Quick start guide
├── GOOGLE_VOICE_SETUP.md         # Google Cloud TTS setup guide
└── assistant_memory.db           # SQLite database (auto-created)
```

---

## 🔧 Configuration

<div align="center">

### **⚙️ Setup Checklist**

- [ ] Install Python 3.13+
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Get Groq API key
- [ ] Create `.env` file
- [ ] (Optional) Setup Google Cloud TTS
- [ ] (Optional) Configure email

</div>

### Groq API Setup

1. Sign up at [Groq Console](https://console.groq.com/)
2. Create an API key
3. Add to `.env`:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Google Cloud TTS (Optional - for best voice quality)

See `GOOGLE_VOICE_SETUP.md` for detailed instructions.

1. Create Google Cloud project
2. Enable Text-to-Speech API
3. Download credentials JSON
4. Set environment variable:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   ```

### Email Setup (Optional)

For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password
3. Add to `.env`:
   ```env
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

---

## 🎨 UI Features

<div align="center">

### **🖥️ Cybernetic Interface**

> **Futuristic design meets powerful functionality**

</div>

### Cybernetic Interface

- **Futuristic Design**: Cybernetic aesthetic with neon accents
- **Real-time Metrics**: CPU, Memory, Neural Load, Bandwidth
- **System Status**: Connection, latency, uptime monitoring
- **Activity Logs**: Terminal-style activity feed
- **Geometric Avatar**: Animated AI avatar with speaking animation
- **Audio Visualization**: Waveform display for voice input
- **Neural Matrix**: LED panel visualization

### Interactive Panels

- **Pomodoro Timer**: Start/stop timer with task tracking
- **Health Tracker**: Quick water and exercise logging
- **Tasks & Reminders**: Manage tasks and set reminders
- **Voice Controls**: Activate voice, switch languages
- **System Metrics**: Real-time performance monitoring

---

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- Store API keys securely
- Review automation actions before execution
- Be cautious with file deletion operations
- Keyboard/mouse automation has failsafe (move mouse to corner to abort)

---

## 🐛 Troubleshooting

### Voice Recognition Not Working
- Check microphone permissions in browser
- Ensure microphone is connected
- Try refreshing the page
- Check browser console for errors

### Groq API Errors
- Verify API key is correct in `.env`
- Check API quota/limits
- Ensure internet connection is active
- Restart Flask server after changing `.env`

### Keyboard/Mouse Automation Fails
- Ensure PyAutoGUI is installed: `pip install pyautogui`
- Check if mouse/keyboard are accessible
- Move mouse to screen corner to abort if needed

### Module Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.11+)
- Try restarting the server

### Database Errors
- Ensure write permissions in project directory
- Delete `assistant_memory.db` to reset (will lose all data)
- Check if SQLite3 is available

---

## 📝 Available Action Types

The assistant supports **70+ action types** across 14 categories:

- **File Operations**: `organize_files`, `search_file_content`, `find_duplicates`, `batch_rename`, `compress_image`, `merge_pdfs`
- **Applications**: `open_app`, `open_vscode`, `browse_url`, `search_google`, `search_wikipedia`, `search_youtube`
- **Code Development**: `create_file`, `create_project`, `git_operation`, `run_command`
- **Learning**: `start_study_session`, `end_study_session`, `create_flashcard`, `save_note`
- **System**: `get_system_info`, `take_screenshot`, `copy_clipboard`
- **Productivity**: `start_pomodoro`, `complete_pomodoro`, `create_habit`, `complete_habit`
- **Advanced AI**: `summarize_document`, `translate_text`, `analyze_sentiment`, `generate_code`, `debug_code`
- **Communication**: `send_email`, `send_whatsapp`, `add_contact`, `get_contact`, `save_linkedin_draft`
- **Web Scraping**: `scrape_website`, `extract_to_excel`
- **Health**: `log_water`, `log_exercise`
- **Keyboard & Mouse**: `type_text`, `press_key`, `click_mouse`, `move_mouse`, `search_in_app`, `navigate_keyboard`, `perform_sequence`
- **Tasks**: `set_reminder`, `create_task`

---

## 🚀 Advanced Features

### Autonomous Operations

JARVIS can execute complex multi-step tasks:
```
"Handle my morning routine" → Opens email, checks calendar, reads reminders
"Organize my downloads folder" → Sorts files by type, removes duplicates
"Prepare for my presentation" → Opens files, checks timing, creates checklist
```

### Persistent Memory

- **Conversation History**: All chats stored in SQLite
- **Task Persistence**: Tasks survive app restarts
- **User Profile**: Remembers your preferences and projects
- **Learning Data**: Flashcards and study sessions persisted

### Smart Scheduling

- **Recurring Reminders**: Set daily, weekly, monthly reminders
- **Background Jobs**: Automated task checking
- **Voice Notifications**: Reminders announced via voice

---

## 📊 Modules Overview

### Core Modules (4)
1. **Groq Agent**: AI reasoning and response generation
2. **Voice Module**: Speech recognition and synthesis
3. **Automation Module**: Desktop control and actions
4. **Memory Module**: Database and persistence

### Feature Modules (10)
5. **Code Module**: Development tools
6. **Learning Module**: Study and research tools
7. **System Module**: Monitoring and utilities
8. **File Advanced Module**: Advanced file operations
9. **Productivity Module**: Timers and habits
10. **AI Advanced Module**: AI-powered features
11. **Communication Module**: Contacts and messaging
12. **Web Scraping Module**: Data extraction
13. **Health Module**: Wellness tracking
14. **Input Automation Module**: Keyboard/mouse control

### Support Modules (2)
15. **Scheduler Module**: Reminders and jobs
16. **Flask App**: Web server and API

---

## 🤝 Contributing

<div align="center">

### **💡 We Welcome Contributions!**

Contributions make the open-source community an amazing place to learn, inspire, and create.

</div>

**Areas for improvement:**
- 🚀 Additional automation features
- 🎨 UI/UX enhancements  
- ⚡ Performance optimizations
- 📖 Documentation improvements
- 🐛 Bug fixes and testing

**How to contribute:**
1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

---

<div align="center">

**Every contribution, no matter how small, is appreciated!** 🙏

</div>

---

## 📄 License

This project is open-source and available for personal and educational use.

---

## 👨‍💻 Author & Credits

<div align="center">

### **Created by Anas Raheem**

🎓 **AI Student & Developer** | 🚀 **Full-Stack Developer** | 🤖 **AI Enthusiast**

[![Website](https://img.shields.io/badge/Website-obrixlabs.com-FF6B6B?style=for-the-badge&logo=google-chrome&logoColor=white)](https://obrixlabs.com)
[![Email](https://img.shields.io/badge/Email-anasraheem.com@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:anasraheem.com@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-anaraheemdev-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/anaraheemdev)
[![Instagram](https://img.shields.io/badge/Instagram-anasraheem.dev-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/anasraheem.dev)

---

**📧 Contact:** [anasraheem.com@gmail.com](mailto:anasraheem.com@gmail.com)  
**🌐 Website:** [obrixlabs.com](https://obrixlabs.com)  
**💼 LinkedIn:** [linkedin.com/in/anaraheemdev](https://linkedin.com/in/anaraheemdev)  
**📷 Instagram:** [@anasraheem.dev](https://instagram.com/anasraheem.dev)

</div>

---

## 🙏 Acknowledgments

<div align="center">

### **Special Thanks To:**

| 🏢 **Organization** | 🎯 **Contribution** |
|---|---|
| [**Groq**](https://groq.com/) | 🔥 Powerful LLM inference API |
| [**Google Cloud**](https://cloud.google.com/) | 🎤 Text-to-Speech API |
| [**Open Source Community**](https://github.com/) | 🛠️ Amazing tools & libraries |
| **All Contributors** | 💚 Code improvements & feedback |

**Thank you for making this project possible!** 🙏

</div>

---

## 📞 Support

<div align="center">

### **🆘 Need Help?**

</div>

**For issues, questions, or suggestions:**

1. 📖 Check the [Troubleshooting](#-troubleshooting) section
2. 📝 Review error logs in the console
3. 🌐 Check browser console for frontend errors
4. 📦 Ensure all dependencies are installed

**Or reach out directly:**
- 📧 Email: [anasraheem.com@gmail.com](mailto:anasraheem.com@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/anaraheemdev](https://linkedin.com/in/anaraheemdev)

---

## 🎯 Quick Links

<div align="center">

| 📚 **Documentation** | 🔗 **Links** |
|---|---|
| 📖 Quick Start Guide | [`QUICKSTART.md`](QUICKSTART.md) |
| 🎤 Google Voice Setup | [`GOOGLE_VOICE_SETUP.md`](GOOGLE_VOICE_SETUP.md) |
| 🌐 Access Dashboard | [http://127.0.0.1:5000](http://127.0.0.1:5000) |
| 🤖 Groq Console | [console.groq.com](https://console.groq.com/) |
| 🌍 Author Website | [obrixlabs.com](https://obrixlabs.com) |

</div>

---

---

<div align="center">

## 📊 **Project Statistics**

| Metric | Status |
|--------|--------|
| **Version** | `3.7` (Cybernetic Interface) |
| **Status** | ✅ Fully Operational |
| **Modules** | 16/16 Loaded |
| **Features** | 100+ Active |
| **Action Types** | 70+ Supported |
| **Languages** | English, Urdu |

---

## 🎨 **Visual Showcase**

```
  ╔════════════════════════════════════════╗
  ║     JARVIS AI DESKTOP ASSISTANT        ║
  ║                                          ║
  ║  🎤 Voice Control    🧠 AI Intelligence ║
  ║  ⌨️  Automation      📊 System Monitor ║
  ║  💻 Code Dev         📚 Learning Tools  ║
  ║  ⏰ Productivity     💪 Health Tracking ║
  ║                                          ║
  ║     Ready to Assist You! 🚀             ║
  ╚════════════════════════════════════════╝
```

---

## 🌟 **Star History**

If you find this project helpful, please consider giving it a ⭐!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-desktop-assistant.svg?style=social&label=Star)](https://github.com/yourusername/ai-desktop-assistant)

---

**Built with ❤️ by [Anas Raheem](https://obrixlabs.com)**

**Version**: `3.7` (Cybernetic Interface) • **Status**: ✅ Fully Operational

---

### 📞 **Get in Touch**

Have questions or suggestions? Feel free to reach out!

- 📧 **Email**: [anasraheem.com@gmail.com](mailto:anasraheem.com@gmail.com)
- 🌐 **Website**: [obrixlabs.com](https://obrixlabs.com)
- 💼 **LinkedIn**: [linkedin.com/in/anaraheemdev](https://linkedin.com/in/anaraheemdev)
- 📷 **Instagram**: [@anasraheem.dev](https://instagram.com/anasraheem.dev)

---

<div align="center">

**Enjoy your AI Desktop Assistant! 🚀**

*JARVIS is ready to assist you with any task.*

Made with 💚 by [Anas Raheem](https://obrixlabs.com)

</div>

