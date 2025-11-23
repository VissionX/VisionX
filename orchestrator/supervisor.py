import time
import threading
from domain.usecases import ProcessFrameUseCase, GenerateDescriptionUseCase
from services.camera import OpenCVCamera
from services.vision import YOLOVisionService
from services.audio import Pyttsx3TTS
from services.speech_recognition import VoskSpeechRecognition
from infra.config import Config

class VisionSupervisor:
    """Main orchestrator for the VisionX application"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize services
        self.camera = OpenCVCamera(config.CAMERA_ID)
        self.vision = YOLOVisionService(
            model_name=config.YOLO_MODEL,
            confidence_threshold=config.CONFIDENCE_THRESHOLD
        )
        self.tts = Pyttsx3TTS()
        self.speech_recognition = VoskSpeechRecognition(
            model_path=config.VOSK_MODEL_PATH,
            sample_rate=config.SAMPLE_RATE,
            trigger_words=config.TRIGGER_WORDS
        )
        
        # Initialize use cases
        self.process_frame_usecase = ProcessFrameUseCase(self.vision)
        self.generate_description_usecase = GenerateDescriptionUseCase()
        
        # State
        self.is_active = False
        self.last_detection_time = 0
        self.status_callback = None
        
    def initialize(self):
        """Initialize all services"""
        print("Initializing VisionX...")
        self.tts.speak("Vision X initializing", block=True)
        
        # Warm up vision model
        print("Loading AI model...")
        self.vision.warm_up()
        
        print("Ready!")
        self.tts.speak("Ready. Say start to detect objects", block=True)
    
    def start(self, status_callback=None):
        """Start the supervisor"""
        self.status_callback = status_callback
        self.is_active = True
        
        # Start listening for voice commands
        self.speech_recognition.start_listening(self._on_voice_command)
        
        if self.status_callback:
            self.status_callback("Listening for voice commands...")
    
    def _on_voice_command(self, command):
        """Handle voice command"""
        print(f"Voice command: {command.text}")
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_detection_time < self.config.DETECTION_COOLDOWN:
            print("Cooldown active, ignoring command")
            return
        
        self.last_detection_time = current_time
        
        # Run detection in separate thread to not block recognition
        threading.Thread(target=self._perform_detection, daemon=True).start()
    
    def _perform_detection(self):
        """Perform object detection"""
        try:
            if self.status_callback:
                self.status_callback("Detecting objects...")
            
            self.tts.speak("Detecting")
            
            # Open camera
            self.camera.open()
            
            # Capture frame
            frame = self.camera.read_frame()
            
            # Process frame
            result = self.process_frame_usecase.execute(frame)
            
            # Generate description
            description = self.generate_description_usecase.execute(result.detections)
            
            print(f"Detected: {description}")
            print(f"Objects: {result.detections}")
            
            # Speak result
            self.tts.speak(description)
            
            if self.status_callback:
                self.status_callback(f"Detected: {description}")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            self.tts.speak("Detection error")
            
            if self.status_callback:
                self.status_callback(error_msg)
        
        finally:
            # Always release camera
            try:
                self.camera.release()
            except:
                pass
            
            if self.status_callback:
                self.status_callback("Listening for voice commands...")
    
    def stop(self):
        """Stop the supervisor"""
        self.is_active = False
        
        # Stop services
        self.speech_recognition.stop_listening()
        self.camera.release()
        self.tts.stop()
        
        print("VisionX stopped")
    
    def __del__(self):
        self.stop()
