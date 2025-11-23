import vosk
import sounddevice as sd
import json
import queue
import threading
from domain.entities import VoiceCommand
import time

class VoskSpeechRecognition:
    """Vosk offline speech recognition"""
    
    def __init__(self, model_path="model", sample_rate=16000, trigger_words=None):
        """
        Initialize Vosk speech recognition
        
        Args:
            model_path: Path to Vosk model directory
            sample_rate: Audio sample rate
            trigger_words: List of words that trigger detection (e.g., ['start', 'detect'])
        """
        self.model = vosk.Model(model_path)
        self.sample_rate = sample_rate
        self.trigger_words = trigger_words or ['start', 'detect', 'see', 'look']
        
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.callback = None
        self.stream = None
        
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio input"""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def start_listening(self, callback):
        """
        Start listening for voice commands
        
        Args:
            callback: Function to call when trigger word is detected
        """
        if self.is_listening:
            return
        
        self.callback = callback
        self.is_listening = True
        
        # Start audio stream
        self.stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Start recognition thread
        self.recognition_thread = threading.Thread(target=self._recognition_worker, daemon=True)
        self.recognition_thread.start()
    
    def _recognition_worker(self):
        """Worker thread for speech recognition"""
        recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
        
        while self.is_listening:
            try:
                data = self.audio_queue.get(timeout=0.5)
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get('text', '').lower()
                    
                    if text:
                        print(f"Recognized: {text}")
                        
                        # Check for trigger words
                        if any(word in text for word in self.trigger_words):
                            command = VoiceCommand(
                                text=text,
                                confidence=1.0,
                                timestamp=time.time()
                            )
                            
                            if self.callback:
                                self.callback(command)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Recognition error: {e}")
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        if hasattr(self, 'recognition_thread'):
            self.recognition_thread.join(timeout=1.0)
    
    def __del__(self):
        self.stop_listening()
