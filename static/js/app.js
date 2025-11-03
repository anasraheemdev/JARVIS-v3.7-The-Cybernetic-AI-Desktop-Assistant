// Cybernetic AI Assistant JavaScript

let currentLanguage = 'en';
let isListening = false;
let recognition = null;
let mediaRecorder = null;
let audioChunks = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeVoiceRecognition();
    setupEventListeners();
    loadTasks();
    loadReminders();
    loadActivityLogs();
    loadSystemMetrics();
    loadProductivityStats();
    loadHealthStats();
    animateSystemMetrics();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadTasks();
        loadReminders();
        loadActivityLogs();
        loadSystemMetrics();
        loadProductivityStats();
        loadHealthStats();
    }, 30000);
    
    // Animate meters every 5 seconds
    setInterval(animateSystemMetrics, 5000);
    
    // Update health and productivity every 10 seconds
    setInterval(() => {
        loadProductivityStats();
        loadHealthStats();
    }, 10000);
});

// Initialize Web Speech API for browser-based voice recognition
function initializeVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = currentLanguage === 'en' ? 'en-US' : 'ur-PK';
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chatInput').value = transcript;
            sendMessage();
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            stopListening();
            showNotification('Voice recognition error. Please try again.', 'error');
        };
        
        recognition.onend = function() {
            if (isListening) {
                recognition.start();
            }
        };
    }
}

// Setup event listeners
function setupEventListeners() {
    // Send button
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    
    // Enter key in input
    document.getElementById('chatInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Voice toggle button
    document.getElementById('voiceToggle').addEventListener('click', toggleVoiceListening);
    
    // Language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentLanguage = this.dataset.lang;
            document.getElementById('currentLang').textContent = currentLanguage === 'en' ? 'ENGLISH' : 'URDU';
            if (recognition) {
                recognition.lang = currentLanguage === 'en' ? 'en-US' : 'ur-PK';
            }
        });
    });
    
    // Add task button
    document.getElementById('addTaskBtn').addEventListener('click', function() {
        document.getElementById('taskModal').classList.remove('hidden');
    });
    
    // Save task button
    document.getElementById('saveTaskBtn').addEventListener('click', addTask);
    
    // Add reminder button
    document.getElementById('addReminderBtn').addEventListener('click', function() {
        document.getElementById('reminderModal').classList.remove('hidden');
    });
    
    // Save reminder button
    document.getElementById('saveReminderBtn').addEventListener('click', addReminder);
    
    // Pomodoro buttons
    const startPomodoroBtn = document.getElementById('startPomodoroBtn');
    const stopPomodoroBtn = document.getElementById('stopPomodoroBtn');
    if (startPomodoroBtn) {
        startPomodoroBtn.addEventListener('click', startPomodoro);
    }
    if (stopPomodoroBtn) {
        stopPomodoroBtn.addEventListener('click', stopPomodoro);
    }
    
    // Health buttons
    const logWaterBtn = document.getElementById('logWaterBtn');
    const logExerciseBtn = document.getElementById('logExerciseBtn');
    if (logWaterBtn) {
        logWaterBtn.addEventListener('click', logWater);
    }
    if (logExerciseBtn) {
        logExerciseBtn.addEventListener('click', logExercise);
    }
    
    // Clear chat button
    if (document.getElementById('clearChatBtn')) {
        document.getElementById('clearChatBtn').addEventListener('click', function() {
            document.getElementById('chatMessages').innerHTML = `
                <div class="terminal-line assistant-msg">
                    <span class="terminal-prompt">&gt;</span> <span class="assistant-text">Chat cleared. Ready for new input.</span>
                </div>
            `;
        });
    }
    
    // Refresh button
    if (document.getElementById('refreshBtn')) {
        document.getElementById('refreshBtn').addEventListener('click', function() {
            loadTasks();
            loadReminders();
            loadActivityLogs();
            showTerminalMessage(document.getElementById('activityLogs'), 'System refreshed');
        });
    }
    
    // Close modals
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.modal-cyber').classList.add('hidden');
        });
    });
    
    // Click outside modal to close
    document.querySelectorAll('.modal-cyber').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.add('hidden');
            }
        });
    });
}

// Toggle voice listening
function toggleVoiceListening() {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

// Update voice button status
function updateVoiceButtonStatus(listening) {
    const voiceBtn = document.getElementById('voiceToggle');
    const voiceBtnText = document.getElementById('voiceBtnText');
    const avatar = document.getElementById('avatarGeometric');
    const waveform = document.getElementById('audioWaveform');
    const voiceStatusEl = document.getElementById('voiceStatus');
    const voiceModeEl = document.getElementById('voiceMode');
    
    if (listening) {
        voiceBtn.classList.add('active');
        if (voiceBtnText) voiceBtnText.textContent = '■ STOP VOICE';
        if (avatar) avatar.classList.add('listening');
        if (waveform) waveform.classList.add('active');
        if (voiceStatusEl) voiceStatusEl.textContent = 'LISTENING';
        if (voiceModeEl) voiceModeEl.textContent = 'ACTIVE';
        document.getElementById('neuralStatus').textContent = 'VOICE INPUT ACTIVE';
    } else {
        voiceBtn.classList.remove('active');
        if (voiceBtnText) voiceBtnText.textContent = '▶ ACTIVATE VOICE';
        if (avatar) avatar.classList.remove('listening');
        if (waveform) waveform.classList.remove('active');
        if (voiceStatusEl) voiceStatusEl.textContent = 'STANDBY';
        if (voiceModeEl) voiceModeEl.textContent = 'INACTIVE';
        document.getElementById('neuralStatus').textContent = 'NEURAL LINK ACTIVE';
    }
}

// Start listening
function startListening() {
    if (recognition) {
        try {
            recognition.start();
            isListening = true;
            updateVoiceButtonStatus(true);
            showNotification('Voice recognition activated', 'success');
        } catch (e) {
            console.error('Error starting recognition:', e);
            showNotification('Could not start voice listening', 'error');
        }
    } else {
        // Fallback: use file-based recording
        startAudioRecording();
    }
}

// Stop listening
function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
        isListening = false;
        updateVoiceButtonStatus(false);
    }
    
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
}

// Start audio recording (fallback)
async function startAudioRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = function(event) {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = function() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            transcribeAudio(audioBlob);
        };
        
        mediaRecorder.start();
        isListening = true;
        document.getElementById('voiceToggle').classList.add('listening');
        document.getElementById('voiceStatus').textContent = 'Recording...';
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        showNotification('Microphone access denied', 'error');
    }
}

// Transcribe audio using backend
async function transcribeAudio(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('language', currentLanguage);
    
    try {
        const response = await fetch('/api/voice/transcribe', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.text) {
            document.getElementById('chatInput').value = data.text;
            sendMessage();
        }
        
    } catch (error) {
        console.error('Error transcribing audio:', error);
        showNotification('Error transcribing audio', 'error');
    } finally {
        stopListening();
    }
}

// Send chat message
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    input.value = '';
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                language: currentLanguage
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.error) {
            addMessageToChat('assistant', `Error: ${data.error}`);
        } else {
            // Extract clean response text (remove JSON formatting if present)
            let responseText = data.response;
            
            // Function to aggressively clean JSON from response
            function extractCleanResponse(text) {
                if (!text) return '';
                
                // Remove markdown code blocks first
                text = text.replace(/```(?:json)?\s*/g, '').replace(/```\s*$/g, '').trim();
                
                // Check if text contains JSON (starts with { or contains { "response":)
                const jsonMatch = text.match(/\{[\s\S]*"response"[\s\S]*\}/);
                
                if (jsonMatch) {
                    const jsonStr = jsonMatch[0];
                    try {
                        // Try to parse the JSON
                        const parsed = JSON.parse(jsonStr);
                        if (parsed.response) {
                            // Remove the JSON from the original text and use the response field
                            const cleanText = text.replace(/\{[\s\S]*"response"[\s\S]*\}/, '').trim();
                            // If there was natural language before JSON, combine them
                            if (cleanText) {
                                return cleanText + ' ' + parsed.response;
                            }
                            return parsed.response;
                        }
                    } catch (e) {
                        // JSON parse failed, try regex extraction
                        console.log('JSON parse failed, using regex extraction');
                        const responseMatch = jsonStr.match(/"response"\s*:\s*"((?:[^"\\]|\\.)*)"/);
                        if (responseMatch && responseMatch[1]) {
                            // Remove JSON from text and use extracted response
                            const cleanText = text.replace(/\{[\s\S]*"response"[\s\S]*\}/, '').trim();
                            const extractedResponse = responseMatch[1]
                                .replace(/\\"/g, '"')
                                .replace(/\\'/g, "'")
                                .replace(/\\n/g, '\n')
                                .replace(/\\t/g, '\t')
                                .replace(/\\r/g, '\r')
                                .replace(/\\\\/g, '\\');
                            
                            if (cleanText) {
                                return cleanText + ' ' + extractedResponse;
                            }
                            return extractedResponse;
                        }
                    }
                    
                    // If we couldn't extract response from JSON, just remove the JSON part
                    return text.replace(/\{[\s\S]*\}/, '').trim();
                }
                
                // If text is pure JSON (starts with {)
                if (text.trim().startsWith('{')) {
                    try {
                        const parsed = JSON.parse(text);
                        if (parsed.response) {
                            return parsed.response;
                        }
                    } catch (e) {
                        // Try regex extraction
                        const patterns = [
                            /"response"\s*:\s*"((?:[^"\\]|\\.)*)"/,
                            /'response'\s*:\s*'((?:[^'\\]|\\.)*)'/,
                            /"response"\s*:\s*`((?:[^`\\]|\\.)*)`/
                        ];
                        
                        for (const pattern of patterns) {
                            const match = text.match(pattern);
                            if (match && match[1]) {
                                return match[1]
                                    .replace(/\\"/g, '"')
                                    .replace(/\\'/g, "'")
                                    .replace(/\\n/g, '\n')
                                    .replace(/\\t/g, '\t')
                                    .replace(/\\r/g, '\r')
                                    .replace(/\\\\/g, '\\');
                            }
                        }
                    }
                }
                
                // Return text as-is if no JSON found
                return text;
            }
            
            responseText = extractCleanResponse(responseText);
            
            addMessageToChat('assistant', responseText);
            
            // Speak only the clean response text with natural voice
            speakText(responseText, currentLanguage);
            
            // Show action results if any
            if (data.actions && data.actions.length > 0) {
                data.actions.forEach(action => {
                    if (action.success) {
                        showNotification(`Action executed: ${action.action}`, 'success');
                    } else {
                        showNotification(`Action failed: ${action.result}`, 'error');
                    }
                });
            }
        }
        
    } catch (error) {
        removeTypingIndicator(typingId);
        console.error('Error sending message:', error);
        addMessageToChat('assistant', 'Sorry, I encountered an error. Please try again.');
    }
}

// Speak text using natural voice
async function speakText(text, language = 'en') {
    try {
        // Stop listening if active to prevent echo/feedback
        if (isListening) {
            stopListening();
            console.log('Stopped listening to prevent echo during speech');
        }
        
        // Add speaking animation to avatar
        const avatar = document.getElementById('avatarGeometric');
        const waveform = document.getElementById('audioWaveform');
        if (avatar) avatar.classList.add('speaking');
        if (waveform) waveform.classList.add('speaking');
        
        await fetch('/api/speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                language: language
            })
        });
        
        // Remove speaking animation after estimated duration (rough estimate: 100ms per character)
        const estimatedDuration = Math.max(3000, text.length * 100); // Minimum 3 seconds
        setTimeout(() => {
            if (avatar) avatar.classList.remove('speaking');
            if (waveform) waveform.classList.remove('speaking');
        }, estimatedDuration);
        
        // Optional: Auto-resume listening after a delay
        // Uncomment the lines below if you want auto-resume
        // setTimeout(() => {
        //     if (!isListening) {
        //         console.log('Auto-resuming listening after speech');
        //     }
        // }, 3000);
    } catch (error) {
        console.error('Error speaking text:', error);
        // Remove speaking animation on error
        const avatar = document.getElementById('avatarGeometric');
        const waveform = document.getElementById('audioWaveform');
        if (avatar) avatar.classList.remove('speaking');
        if (waveform) waveform.classList.remove('speaking');
    }
}

// ========== CYBERNETIC UI SPECIFIC FUNCTIONS ==========

// Animate system metrics
let pomodoroTimer = null;
let pomodoroStartTime = null;
let pomodoroDuration = 25; // minutes

// Load system metrics (real-time)
async function loadSystemMetrics() {
    try {
        const response = await fetch('/api/system/info');
        const data = await response.json();
        
        if (data.info && !data.info.error) {
            const cpuMeter = document.getElementById('cpuMeter');
            const memoryMeter = document.getElementById('memoryMeter');
            
            if (cpuMeter && data.info.cpu_percent !== undefined) {
                cpuMeter.style.width = data.info.cpu_percent + '%';
            }
            
            if (memoryMeter && data.info.memory) {
                memoryMeter.style.width = data.info.memory.percent + '%';
            }
        }
    } catch (error) {
        console.error('Error loading system metrics:', error);
    }
}

// Load productivity stats
async function loadProductivityStats() {
    try {
        const response = await fetch('/api/productivity/stats');
        const data = await response.json();
        
        if (data.stats) {
            const pomodoroCount = data.stats.pomodoros_today || 0;
            const focusMinutes = data.stats.focus_minutes_today || 0;
            
            // Update UI if elements exist
            const pomodoroStatus = document.getElementById('pomodoroStatus');
            if (pomodoroStatus && !pomodoroTimer) {
                // Update count display somewhere in UI if needed
            }
        }
    } catch (error) {
        console.error('Error loading productivity stats:', error);
    }
}

// Load health stats
async function loadHealthStats() {
    try {
        const response = await fetch('/api/health/stats');
        const data = await response.json();
        
        if (data.stats) {
            const waterElement = document.getElementById('waterIntake');
            const exerciseElement = document.getElementById('exerciseTime');
            
            if (waterElement) {
                waterElement.textContent = data.stats.daily_water_ml + 'ml';
            }
            
            if (exerciseElement) {
                exerciseElement.textContent = data.stats.weekly_exercise_minutes + 'min';
            }
        }
    } catch (error) {
        console.error('Error loading health stats:', error);
    }
}

// Pomodoro timer functions
function startPomodoro() {
    const task = prompt('Enter task name:', 'Work');
    if (!task) return;
    
    pomodoroDuration = parseInt(prompt('Duration in minutes (default 25):', '25')) || 25;
    pomodoroStartTime = Date.now();
    
    const statusEl = document.getElementById('pomodoroStatus');
    const taskEl = document.getElementById('pomodoroTask');
    const timeEl = document.getElementById('pomodoroTime');
    const startBtn = document.getElementById('startPomodoroBtn');
    const stopBtn = document.getElementById('stopPomodoroBtn');
    
    if (statusEl) statusEl.textContent = 'ACTIVE';
    if (taskEl) taskEl.textContent = task.toUpperCase();
    if (startBtn) startBtn.classList.add('hidden');
    if (stopBtn) stopBtn.classList.remove('hidden');
    
    // Send action to backend
    sendMessage(`Start a ${pomodoroDuration}-minute Pomodoro for ${task}`);
    
    // Update timer display
    updatePomodoroTimer();
    pomodoroTimer = setInterval(updatePomodoroTimer, 1000);
}

function stopPomodoro() {
    if (pomodoroTimer) {
        clearInterval(pomodoroTimer);
        pomodoroTimer = null;
    }
    
    const statusEl = document.getElementById('pomodoroStatus');
    const taskEl = document.getElementById('pomodoroTask');
    const timeEl = document.getElementById('pomodoroTime');
    const startBtn = document.getElementById('startPomodoroBtn');
    const stopBtn = document.getElementById('stopPomodoroBtn');
    
    if (statusEl) statusEl.textContent = 'INACTIVE';
    if (taskEl) taskEl.textContent = 'NONE';
    if (timeEl) timeEl.textContent = '00:00';
    if (startBtn) startBtn.classList.remove('hidden');
    if (stopBtn) stopBtn.classList.add('hidden');
    
    // Calculate duration and send completion
    if (pomodoroStartTime) {
        const duration = Math.floor((Date.now() - pomodoroStartTime) / 60000);
        sendMessage(`Complete my Pomodoro. I studied for ${duration} minutes.`);
        pomodoroStartTime = null;
    }
}

function updatePomodoroTimer() {
    if (!pomodoroStartTime) return;
    
    const elapsed = Math.floor((Date.now() - pomodoroStartTime) / 1000);
    const remaining = (pomodoroDuration * 60) - elapsed;
    
    if (remaining <= 0) {
        stopPomodoro();
        alert('Pomodoro complete! Great work!');
        return;
    }
    
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    const timeEl = document.getElementById('pomodoroTime');
    
    if (timeEl) {
        timeEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
}

// Health logging
function logWater() {
    const amount = prompt('Water amount in ml (default 250):', '250');
    if (amount) {
        sendMessage(`Log ${amount}ml water intake`);
    }
}

function logExercise() {
    const activity = prompt('Exercise activity:', 'Exercise');
    const duration = prompt('Duration in minutes:', '30');
    if (activity && duration) {
        sendMessage(`Log ${duration} minutes of ${activity}`);
    }
}

function animateSystemMetrics() {
    const cpuMeter = document.getElementById('cpuMeter');
    const neuralMeter = document.getElementById('neuralMeter');
    const memoryMeter = document.getElementById('memoryMeter');
    const bandwidthMeter = document.getElementById('bandwidthMeter');
    
    // If real metrics are not available, use random values
    if (cpuMeter && !cpuMeter.dataset.real) {
        const cpu = Math.floor(Math.random() * 40) + 40; // 40-80%
        cpuMeter.style.width = cpu + '%';
    }
    
    if (neuralMeter) {
        const neural = Math.floor(Math.random() * 30) + 60; // 60-90%
        neuralMeter.style.width = neural + '%';
    }
    
    if (memoryMeter && !memoryMeter.dataset.real) {
        const memory = Math.floor(Math.random() * 35) + 35; // 35-70%
        memoryMeter.style.width = memory + '%';
    }
    
    if (bandwidthMeter) {
        const bandwidth = Math.floor(Math.random() * 20) + 75; // 75-95%
        bandwidthMeter.style.width = bandwidth + '%';
    }
}

// Show terminal message
function showTerminalMessage(terminalElement, message, isError = false) {
    if (!terminalElement) return;
    
    const line = document.createElement('div');
    line.className = 'terminal-line';
    line.innerHTML = `<span class="terminal-prompt">&gt;</span> <span style="color: ${isError ? '#ff0000' : '#00ff00'}">${message}</span>`;
    
    terminalElement.appendChild(line);
    terminalElement.scrollTop = terminalElement.scrollHeight;
    
    // Keep only last 20 messages
    while (terminalElement.children.length > 20) {
        terminalElement.removeChild(terminalElement.firstChild);
    }
}

// Override addMessageToChat for terminal style
const originalAddMessageToChat = window.addMessageToChat || function() {};
window.addMessageToChat = function(role, message) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const line = document.createElement('div');
    line.className = `terminal-line ${role === 'assistant' ? 'assistant-msg' : 'user-msg'}`;
    
    if (role === 'user') {
        line.innerHTML = `<span class="terminal-prompt">&gt;</span> <span class="user-text">[USER]: ${escapeHtml(message)}</span>`;
    } else {
        line.innerHTML = `<span class="terminal-prompt">&gt;</span> <span class="assistant-text">[JARVIS]: ${escapeHtml(message)}</span>`;
    }
    
    chatMessages.appendChild(line);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Keep only last 50 messages
    while (chatMessages.children.length > 50) {
        chatMessages.removeChild(chatMessages.firstChild);
    }
};

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Override showTypingIndicator
window.showTypingIndicator = function() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return null;
    
    const line = document.createElement('div');
    line.className = 'terminal-line assistant-msg';
    line.id = 'typing-indicator';
    line.innerHTML = `<span class="terminal-prompt">&gt;</span> <span class="assistant-text">[JARVIS]: Processing...</span>`;
    
    chatMessages.appendChild(line);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return 'typing-indicator';
};

// Override removeTypingIndicator
window.removeTypingIndicator = function(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
};

// Override showNotification for cyber UI
window.showNotification = function(message, type = 'info') {
    const activityLogs = document.getElementById('activityLogs');
    if (activityLogs) {
        showTerminalMessage(activityLogs, message, type === 'error');
    }
    console.log(`[${type.toUpperCase()}] ${message}`);
};

// Override renderTask for terminal style
window.renderTask = function(task) {
    return `
        <div class="task-item ${task.completed ? 'completed' : ''}" data-task-id="${task.id}">
            <span class="terminal-prompt">&gt;</span> ${escapeHtml(task.task_text)}
            ${task.due_date ? ` [${task.due_date}]` : ''}
            <span style="float: right; cursor: pointer;" onclick="deleteTask(${task.id})">✕</span>
        </div>
    `;
};

// Override renderReminder for terminal style
window.renderReminder = function(reminder) {
    return `
        <div class="reminder-item" data-reminder-id="${reminder.id}">
            <span class="terminal-prompt">&gt;</span> ${escapeHtml(reminder.reminder_text)}
            [${reminder.reminder_time}]
            <span style="float: right; cursor: pointer;" onclick="deleteReminder(${reminder.id})">✕</span>
        </div>
    `;
};

// Add message to chat UI
function addMessageToChat(role, content) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `${role}-message message-slide-in`;
    
    const timestamp = new Date().toLocaleTimeString().toUpperCase();
    
    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="message-avatar">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center bg-gradient-to-r from-purple-500 to-pink-600 border-2 border-purple-400">
                        <span class="text-xs font-bold font-mono">YOU</span>
                    </div>
                </div>
                <div class="flex-1">
                    <p class="text-purple-100 leading-relaxed">${escapeHtml(content)}</p>
                    <p class="text-xs text-purple-400 mt-1 font-mono">${timestamp}</p>
                </div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="message-avatar">
                    <div class="avatar-mini-glow"></div>
                    <svg class="w-8 h-8" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="50" cy="35" r="15" fill="url(#avatarGradient)" opacity="0.8"/>
                        <path d="M 30 45 Q 50 55 70 45 L 70 60 Q 50 75 30 60 Z" fill="url(#avatarGradient)" opacity="0.8"/>
                    </svg>
                </div>
                <div class="flex-1">
                    <p class="text-cyan-100 leading-relaxed">${escapeHtml(content)}</p>
                    <p class="text-xs text-cyan-500 mt-1 font-mono">${timestamp}</p>
                </div>
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    const typingId = 'typing-' + Date.now();
    typingDiv.id = typingId;
    typingDiv.className = 'assistant-message message-slide-in';
    
    typingDiv.innerHTML = `
        <div class="flex items-start space-x-3">
            <div class="message-avatar">
                <div class="avatar-mini-glow"></div>
                <svg class="w-8 h-8" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="35" r="15" fill="url(#avatarGradient)" opacity="0.8"/>
                    <path d="M 30 45 Q 50 55 70 45 L 70 60 Q 50 75 30 60 Z" fill="url(#avatarGradient)" opacity="0.8"/>
                </svg>
            </div>
            <div class="flex-1">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return typingId;
}

// Remove typing indicator
function removeTypingIndicator(typingId) {
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Load tasks
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const data = await response.json();
        
        const tasksList = document.getElementById('tasksList');
        tasksList.innerHTML = '';
        
        if (data.tasks && data.tasks.length > 0) {
            data.tasks.forEach(task => {
                const taskDiv = document.createElement('div');
                taskDiv.className = `task-item ${task.status === 'completed' ? 'completed' : ''}`;
                
                taskDiv.innerHTML = `
                    <div class="flex items-center space-x-2 flex-1">
                        <input type="checkbox" ${task.status === 'completed' ? 'checked' : ''} 
                               onchange="toggleTask(${task.id}, this.checked)">
                        <span class="task-text">${escapeHtml(task.task_text)}</span>
                    </div>
                    <button onclick="deleteTask(${task.id})" class="text-red-400 hover:text-red-300">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                `;
                
                tasksList.appendChild(taskDiv);
            });
        } else {
            tasksList.innerHTML = '<p class="text-gray-400 text-sm">No tasks yet</p>';
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

// Load reminders
async function loadReminders() {
    try {
        const response = await fetch('/api/reminders');
        const data = await response.json();
        
        const remindersList = document.getElementById('remindersList');
        remindersList.innerHTML = '';
        
        if (data.reminders && data.reminders.length > 0) {
            data.reminders.forEach(reminder => {
                const reminderDiv = document.createElement('div');
                reminderDiv.className = 'reminder-item';
                
                const reminderTime = new Date(reminder.reminder_time);
                reminderDiv.innerHTML = `
                    <div class="flex-1">
                        <p class="text-sm">${escapeHtml(reminder.reminder_text)}</p>
                        <p class="text-xs text-gray-400">${reminderTime.toLocaleString()}</p>
                    </div>
                `;
                
                remindersList.appendChild(reminderDiv);
            });
        } else {
            remindersList.innerHTML = '<p class="text-gray-400 text-sm">No reminders yet</p>';
        }
    } catch (error) {
        console.error('Error loading reminders:', error);
    }
}

// Load activity logs
async function loadActivityLogs() {
    try {
        const response = await fetch('/api/logs');
        const data = await response.json();
        
        const logsDiv = document.getElementById('activityLogs');
        logsDiv.innerHTML = '';
        
        if (data.logs && data.logs.length > 0) {
            data.logs.slice(0, 10).forEach(log => {
                const logDiv = document.createElement('div');
                logDiv.className = 'activity-item';
                
                const logTime = new Date(log.timestamp);
                logDiv.innerHTML = `
                    <p class="font-semibold">${log.action_type}</p>
                    <p class="text-xs text-gray-400">${logTime.toLocaleString()}</p>
                `;
                
                logsDiv.appendChild(logDiv);
            });
        } else {
            logsDiv.innerHTML = '<p class="text-gray-400 text-sm">No activity yet</p>';
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

// Add task
async function addTask() {
    const taskText = document.getElementById('taskInput').value.trim();
    const dueDateInput = document.getElementById('taskDueDate').value;
    
    if (!taskText) {
        showNotification('Please enter a task', 'error');
        return;
    }
    
    // Convert datetime-local format to ISO format if provided
    const dueDate = dueDateInput ? new Date(dueDateInput).toISOString() : null;
    
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: taskText,
                due_date: dueDate
            })
        });
        
        const data = await response.json();
        
        if (data.task_id) {
            document.getElementById('taskModal').classList.add('hidden');
            document.getElementById('taskInput').value = '';
            document.getElementById('taskDueDate').value = '';
            loadTasks();
            showNotification('Task added successfully', 'success');
        }
    } catch (error) {
        console.error('Error adding task:', error);
        showNotification('Error adding task', 'error');
    }
}

// Add reminder
async function addReminder() {
    const reminderText = document.getElementById('reminderInput').value.trim();
    const reminderTimeInput = document.getElementById('reminderTime').value;
    
    if (!reminderText || !reminderTimeInput) {
        showNotification('Please fill all fields', 'error');
        return;
    }
    
    // Convert datetime-local format to ISO format
    const reminderTime = new Date(reminderTimeInput).toISOString();
    
    try {
        const response = await fetch('/api/reminders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reminder: reminderText,
                time: reminderTime
            })
        });
        
        const data = await response.json();
        
        if (data.reminder_id) {
            document.getElementById('reminderModal').classList.add('hidden');
            document.getElementById('reminderInput').value = '';
            document.getElementById('reminderTime').value = '';
            loadReminders();
            showNotification('Reminder added successfully', 'success');
        }
    } catch (error) {
        console.error('Error adding reminder:', error);
        showNotification('Error adding reminder', 'error');
    }
}

// Toggle task completion
async function toggleTask(taskId, completed) {
    try {
        await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: completed ? 'completed' : 'pending'
            })
        });
        
        loadTasks();
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        loadTasks();
        showNotification('Task deleted', 'success');
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type = 'info') {
    // Simple notification (can be enhanced with a toast library)
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    } text-white`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Make functions globally available
window.toggleTask = toggleTask;
window.deleteTask = deleteTask;

