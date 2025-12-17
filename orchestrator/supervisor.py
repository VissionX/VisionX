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
        print(f"VisionSupervisor.__init__ called with config type: {type(config)}")
        self.config = config
        self._initialized = False
        
        # Initialize services
        print("Initializing camera...")
        self.camera = OpenCVCamera(config.CAMERA_ID)
        
        print("Initializing YOLO vision...")
        self.vision = YOLOVisionService(
            model_name=config.YOLO_MODEL,
            confidence_threshold=config.CONFIDENCE_THRESHOLD
        )
        
        print("Initializing TTS...")
        self.tts = Pyttsx3TTS()
        
        print("Initializing speech recognition...")
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
        
        print("VisionSupervisor.__init__ completed successfully")
        
    def initialize(self):
        """Initialize all services"""
        print("=== INITIALIZATION START ===")
        print("Step 1: Speaking initialization message...")
        
        try:
            self.tts.speak("Vision X initializing", block=False)
            print("✓ TTS queued")
        except Exception as e:
            print(f"⚠ TTS error (non-fatal): {e}")
        
        # Warm up vision model
        print("Step 2: Warming up YOLO model...")
        try:
            self.vision.warm_up()
            print("✓ YOLO warmed up")
        except Exception as e:
            print(f"❌ YOLO warm-up failed: {e}")
            raise
        
        self._initialized = True
        print("Step 3: Initialization complete!")
        
        # Speak ready message
        try:
            self.tts.speak("Ready. Say start to detect objects", block=False)
            print("✓ Ready message queued")
        except Exception as e:
            print(f"⚠ TTS error (non-fatal): {e}")
        
        print("=== INITIALIZATION COMPLETE ===")
    
    def start(self, status_callback=None):
        """Start the supervisor"""
        print("=== STARTING SUPERVISOR ===")
        self.status_callback = status_callback
        self.is_active = True
        
        # Start listening for voice commands
        print("Starting speech recognition listener...")
        try:
            self.speech_recognition.start_listening(self._on_voice_command)
            print("✓ Speech recognition started!")
        except Exception as e:
            print(f"❌ Speech recognition failed: {e}")
            raise
        
        if self.status_callback:
            self.status_callback("Listening for voice commands...")
        
        print(f"✓ Listening for trigger words: {self.config.TRIGGER_WORDS}")
        print("=== SUPERVISOR READY ===")
        print("\n💬 Say 'START' to detect objects!\n")
    
    def _on_voice_command(self, command):
        """Handle voice command"""
        print(f"\n🎯 Voice command received: '{command.text}'")
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_detection_time < self.config.DETECTION_COOLDOWN:
            remaining = self.config.DETECTION_COOLDOWN - (current_time - self.last_detection_time)
            print(f"⏳ Cooldown active ({remaining:.1f}s remaining), ignoring command")
            return
        
        self.last_detection_time = current_time
        print("✓ Cooldown OK, starting detection...")
        
        # Run detection in separate thread to not block recognition
        threading.Thread(target=self._perform_detection, daemon=True).start()
    
    def _perform_detection(self):
        """Perform object detection"""
        print("\n" + "="*50)
        print("DETECTION CYCLE START")
        print("="*50)
        
        try:
            if self.status_callback:
                self.status_callback("Detecting objects...")
            
            print("Step 1: Speaking 'Detecting'...")
            self.tts.speak("Detecting")
            
            print("Step 2: Opening camera...")
            self.camera.open()
            print("✓ Camera opened")
            
            print("Step 3: Capturing frame...")
            frame = self.camera.read_frame()
            print(f"✓ Frame captured: {frame.frame.shape}")
            
            print("Step 4: Running YOLO detection...")
            result = self.process_frame_usecase.execute(frame)
            print(f"✓ Detection complete: {len(result.detections)} objects found")
            
            print("Step 5: Generating description...")
            description = self.generate_description_usecase.execute(result.detections)
            print(f"✓ Description: '{description}'")
            
            print("\nDetected objects:")
            for i, det in enumerate(result.detections, 1):
                print(f"  {i}. {det.class_name} ({det.confidence:.2%})")
            
            print(f"\nStep 6: Speaking result...")
            self.tts.speak(description)
            print(f"✓ Spoke: '{description}'")
            
            if self.status_callback:
                self.status_callback(f"Detected: {description}")
            
            print("="*50)
            print("DETECTION CYCLE COMPLETE")
            print("="*50 + "\n")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n❌ DETECTION ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            self.tts.speak("Detection error")
            
            if self.status_callback:
                self.status_callback(error_msg)
        
        finally:
            # Always release camera
            try:
                print("Releasing camera...")
                self.camera.release()
                print("✓ Camera released")
            except Exception as e:
                print(f"⚠ Camera release error: {e}")
            
            if self.status_callback:
                self.status_callback("Listening for voice commands...")
            
            print("\n💬 Ready for next command. Say 'START'!\n")
    
    def stop(self):
        """Stop the supervisor"""
        print("Stopping VisionSupervisor...")
        self.is_active = False
        
        try:
            if hasattr(self, 'speech_recognition'):
                print("Stopping speech recognition...")
                self.speech_recognition.stop_listening()
        except Exception as e:
            print(f"Error stopping speech: {e}")
        
        try:
            if hasattr(self, 'camera'):
                print("Releasing camera...")
                self.camera.release()
        except Exception as e:
            print(f"Error releasing camera: {e}")
        
        try:
            if hasattr(self, 'tts'):
                print("Stopping TTS...")
                self.tts.stop()
        except Exception as e:
            print(f"Error stopping TTS: {e}")
        
        print("VisionX stopped")
    
    def __del__(self):
        if hasattr(self, '_initialized') and self._initialized:
            try:
                print("VisionSupervisor.__del__ called")
                self.stop()
            except:
                pass
