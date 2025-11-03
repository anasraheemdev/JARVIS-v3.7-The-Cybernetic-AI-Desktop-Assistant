"""
Voice Module - Handles Speech-to-Text (STT) and Text-to-Speech (TTS)
Supports English and Urdu
"""

import logging
import threading
import queue
import io
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# Speech Recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    logger.warning("speech_recognition not installed. Install with: pip install SpeechRecognition")

# Google Cloud Text-to-Speech (PRIMARY - Best Quality!)
try:
    from google.cloud import texttospeech
    import os
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False
    logger.warning("Google Cloud TTS not installed. Install with: pip install google-cloud-texttospeech")

# Text-to-Speech - Natural Voice (Fallback)
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logger.warning("pyttsx3 not installed. Install with: pip install pyttsx3")

# Fallback TTS
try:
    from gtts import gTTS
    import pygame
    pygame.mixer.init()
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logger.warning("gTTS not installed. Install with: pip install gtts pygame")

class VoiceModule:
    """Handles voice input and output with multi-language support"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.microphone = None
        self.is_listening = False
        self.listening_thread = None
        self.audio_queue = queue.Queue()
        
        # Google Cloud TTS is our primary engine! (Ultra Natural Human Voice)
        self.google_tts_client = None
        if GOOGLE_TTS_AVAILABLE:
            try:
                # Try to initialize Google Cloud TTS client
                # Note: Requires GOOGLE_APPLICATION_CREDENTIALS env var or default credentials
                self.google_tts_client = texttospeech.TextToSpeechClient()
                logger.info("🎤 Google Cloud TTS initialized as PRIMARY engine (Ultra Natural Voice!)")
            except Exception as e:
                logger.warning(f"Google Cloud TTS not configured (needs credentials): {e}")
                logger.info("Falling back to other TTS engines. Set GOOGLE_APPLICATION_CREDENTIALS to use Google TTS.")
                self.google_tts_client = None
        
        # Initialize Natural TTS (pyttsx3 - offline fallback)
        self.tts_engine = None
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Set properties for more natural voice
                voices = self.tts_engine.getProperty('voices')
                # Try to find a female voice (sounds more natural for assistant)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                self.tts_engine.setProperty('rate', 175)  # Speed (default 200)
                self.tts_engine.setProperty('volume', 0.9)  # Volume (0-1)
                logger.info("pyttsx3 TTS initialized as fallback")
            except Exception as e:
                logger.error(f"Error initializing pyttsx3: {e}")
                self.tts_engine = None
        
        # Initialize microphone
        if self.recognizer:
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing microphone: {e}")
    
    def transcribe_audio(self, audio_file, language: str = 'en') -> Tuple[str, str]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file: Audio file object or file path
            language: Language code ('en' for English, 'ur' for Urdu)
        
        Returns:
            tuple: (transcribed_text, detected_language)
        """
        if not self.recognizer:
            return "Speech recognition not available", language
        
        try:
            # Handle different input types
            if isinstance(audio_file, str):
                # File path
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            else:
                # File-like object (Flask upload)
                audio_data = audio_file.read()
                audio_file.seek(0)
                
                # Convert to WAV if needed
                audio = sr.AudioData(audio_data, 16000, 2)
            
            # Try Google Speech Recognition
            try:
                # Map language codes
                lang_code = 'en-US' if language == 'en' else 'ur-PK'
                
                text = self.recognizer.recognize_google(audio, language=lang_code)
                return text, language
            
            except sr.UnknownValueError:
                return "Could not understand audio", language
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                return f"Error with speech recognition service: {e}", language
        
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return f"Error: {str(e)}", language
    
    def listen_once(self, language: str = 'en', timeout: int = 5) -> Tuple[Optional[str], str]:
        """
        Listen for speech once
        
        Args:
            language: Language code
            timeout: Timeout in seconds
        
        Returns:
            tuple: (transcribed_text, detected_language)
        """
        if not self.recognizer or not self.microphone:
            return None, language
        
        try:
            with self.microphone as source:
                logger.info(f"Listening for {timeout} seconds...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            lang_code = 'en-US' if language == 'en' else 'ur-PK'
            
            try:
                text = self.recognizer.recognize_google(audio, language=lang_code)
                logger.info(f"Recognized: {text}")
                return text, language
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None, language
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                return None, language
        
        except sr.WaitTimeoutError:
            logger.info("Listening timeout")
            return None, language
        except Exception as e:
            logger.error(f"Error in listen_once: {e}")
            return None, language
    
    def start_listening(self, callback=None, language: str = 'en'):
        """Start continuous listening in a background thread"""
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        if not self.recognizer or not self.microphone:
            logger.error("Microphone not available")
            return
        
        self.is_listening = True
        
        def listen_loop():
            while self.is_listening:
                try:
                    text, detected_lang = self.listen_once(language, timeout=1)
                    if text and callback:
                        callback(text, detected_lang)
                except Exception as e:
                    logger.error(f"Error in listening loop: {e}")
                    if not self.is_listening:
                        break
        
        self.listening_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listening_thread.start()
        logger.info("Started continuous listening")
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self.listening_thread:
            self.listening_thread.join(timeout=2)
        logger.info("Stopped listening")
    
    def speak(self, text: str, language: str = 'en', slow: bool = False):
        """
        Convert text to speech and play it with ULTRA NATURAL human voice
        
        Args:
            text: Text to speak
            language: Language code ('en' or 'ur')
            slow: Whether to speak slowly
        """
        try:
            if not text:
                return
            
            # PRIORITY 1: Google Cloud TTS - THE BEST QUALITY! (WaveNet/Neural2 voices)
            if self.google_tts_client:
                try:
                    self._speak_google_tts(text, language, slow)
                    return
                except Exception as e:
                    logger.warning(f"Google Cloud TTS failed: {e}")
            
            # PRIORITY 2: Use pyttsx3 for offline English (fallback)
            if PYTTSX3_AVAILABLE and language == 'en':
                try:
                    import pyttsx3
                    import tempfile
                    import os
                    
                    # Use pyttsx3 to save to file instead of speaking directly
                    # This avoids the "run loop already started" error
                    engine = pyttsx3.init()
                    
                    # Set properties
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            engine.setProperty('voice', voice.id)
                            break
                    
                    if slow:
                        engine.setProperty('rate', 150)
                    else:
                        engine.setProperty('rate', 175)
                    engine.setProperty('volume', 0.9)
                    
                    # Save to file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    temp_file.close()
                    
                    engine.save_to_file(text, temp_file.name)
                    engine.runAndWait()
                    
                    # Play with pygame (avoids thread issues)
                    pygame.mixer.music.load(temp_file.name)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                    
                    # Cleanup
                    try:
                        os.remove(temp_file.name)
                    except:
                        pass
                    
                    logger.info("✅ Spoke with pyttsx3 (Fallback)")
                    return
                except Exception as e:
                    logger.warning(f"pyttsx3 failed: {e}")
            
            # LAST RESORT: Fallback to gTTS
            if GTTS_AVAILABLE:
                # Map language codes
                lang_code = 'en' if language == 'en' else 'ur'
                
                # Create TTS object
                tts = gTTS(text=text, lang=lang_code, slow=slow)
                
                # Save to bytes buffer
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                
                # Play audio
                pygame.mixer.music.load(audio_buffer)
                pygame.mixer.music.play()
                
                # Wait for playback
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                logger.info("✅ Spoke with gTTS (Last Resort)")
            else:
                logger.warning("No TTS engine available")
        
        except Exception as e:
            logger.error(f"Error in speak: {e}")
    
    def _speak_google_tts(self, text: str, language: str = 'en', slow: bool = False):
        """Use Google Cloud TTS for ULTRA NATURAL human voice (WaveNet/Neural2)"""
        import tempfile
        import os
        
        try:
            # Set up the input text
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Select voice based on language
            if language == 'ur':
                # Urdu voice (Pakistan)
                voice = texttospeech.VoiceSelectionParams(
                    language_code="ur-PK",
                    name="ur-PK-Wavenet-A",  # WaveNet for best quality
                    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
                )
            else:
                # English voice (US) - Ultra natural!
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    name="en-US-Neural2-F",  # Neural2 - Most natural!
                    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
                )
            
            # Configure audio output
            speaking_rate = 0.9 if slow else 1.0
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
                pitch=0.0,
                volume_gain_db=0.0
            )
            
            # Perform the text-to-speech request
            response = self.google_tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Save audio to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.write(response.audio_content)
            temp_file.close()
            
            # Play the audio
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Cleanup
            try:
                os.remove(temp_file.name)
            except:
                pass
            
            logger.info(f"🎤 ✅ Spoke with Google Cloud TTS ({language.upper()}) - ULTRA NATURAL!")
        
        except Exception as e:
            logger.error(f"Google Cloud TTS error: {e}")
            raise
    
    async def _speak_edge_tts(self, text: str, language: str = 'en'):
        """Use Edge TTS for natural voice (async) - Supports Urdu!"""
        import tempfile
        import os
        
        try:
            # Select voice based on language
            if language == 'ur':
                voice = "ur-PK-AsadNeural"  # Male Urdu voice
                # Alternative: "ur-PK-UzmaNeural"  # Female Urdu voice
            else:
                voice = "en-US-AriaNeural"  # Very natural English voice
            
            # Create communicate object with proper headers
            communicate = edge_tts.Communicate(text, voice, rate="+10%", volume="+10%")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Save with timeout to prevent hanging
            await asyncio.wait_for(communicate.save(temp_file.name), timeout=10.0)
            
            # Play the audio
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Cleanup
            try:
                os.remove(temp_file.name)
            except:
                pass
            
            logger.info(f"✅ Spoke with Edge TTS ({language.upper()})")
        except asyncio.TimeoutError:
            logger.warning("Edge TTS timed out")
            raise Exception("Edge TTS timeout")
        except Exception as e:
            logger.warning(f"Edge TTS error: {e}")
            raise
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text (simple heuristic)
        In production, use proper language detection library
        """
        # Simple heuristic: check for Urdu characters
        urdu_chars = set('ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنوہھءیے')
        
        if any(char in urdu_chars for char in text):
            return 'ur'
        return 'en'

