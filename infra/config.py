import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    
    # Camera settings
    CAMERA_ID: int = 0
    CAMERA_WIDTH: int = 640
    CAMERA_HEIGHT: int = 480
    
    # YOLO settings
    YOLO_MODEL: str = 'yolov8n.pt'  # Use nano model for speed
    CONFIDENCE_THRESHOLD: float = 0.5
    
    # Speech settings
    VOSK_MODEL_PATH: str = 'model'  # Path to Vosk model
    SAMPLE_RATE: int = 16000
    TRIGGER_WORDS: list = None  # Will be set in __post_init__
    
    # TTS settings
    TTS_RATE: int = 150
    TTS_VOLUME: float = 1.0
    
    # Detection settings
    DETECTION_COOLDOWN: float = 3.0  # Seconds between detections
    
    def __post_init__(self):
        if self.TRIGGER_WORDS is None:
            self.TRIGGER_WORDS = ['start', 'detect', 'see', 'look', 'scan']
    
    @classmethod
    def from_env(cls):
        """Load config from environment variables"""
        return cls(
            CAMERA_ID=int(os.getenv('CAMERA_ID', 0)),
            YOLO_MODEL=os.getenv('YOLO_MODEL', 'yolov8n.pt'),
            CONFIDENCE_THRESHOLD=float(os.getenv('CONFIDENCE_THRESHOLD', 0.5)),
            VOSK_MODEL_PATH=os.getenv('VOSK_MODEL_PATH', 'model'),
        )
