import pyttsx3
import threading
import queue
from abc import ABC, abstractmethod

class TTSInterface(ABC):
    """Text-to-speech interface"""
    
    @abstractmethod
    def speak(self, text: str, block=False):
        pass
    
    @abstractmethod
    def stop(self):
        pass

class Pyttsx3TTS(TTSInterface):
    """pyttsx3 TTS implementation (offline)"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed
        self.engine.setProperty('volume', 1.0)  # Volume
        
        # Use a queue for thread-safe speech
        self.speech_queue = queue.Queue()
        self.is_running = True
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
    
    def _speech_worker(self):
        """Worker thread for speech"""
        while self.is_running:
            try:
                text = self.speech_queue.get(timeout=0.5)
                if text is not None:
                    self.engine.say(text)
                    self.engine.runAndWait()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TTS error: {e}")
    
    def speak(self, text: str, block=False):
        """
        Speak text
        
        Args:
            text: Text to speak
            block: If True, wait for speech to complete
        """
        if not text:
            return
        
        # Clear queue and add new text
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
        
        self.speech_queue.put(text)
        
        if block:
            self.speech_queue.join()
    
    def stop(self):
        """Stop TTS engine"""
        self.is_running = False
        self.speech_thread.join(timeout=1.0)
        try:
            self.engine.stop()
        except:
            pass
    
    def __del__(self):
        self.stop()
