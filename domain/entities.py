from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class Detection:
    """Represents a single object detection"""
    class_name: str
    confidence: float
    bbox: tuple  # (x1, y1, x2, y2)
    
    def __str__(self):
        return f"{self.class_name} ({self.confidence:.2f})"

@dataclass
class CameraFrame:
    """Represents a camera frame with timestamp"""
    frame: np.ndarray
    timestamp: float
    detections: Optional[List[Detection]] = None
    
@dataclass
class VoiceCommand:
    """Represents a recognized voice command"""
    text: str
    confidence: float
    timestamp: float
