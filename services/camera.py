import cv2
import time
from abc import ABC, abstractmethod
from domain.entities import CameraFrame

class CameraInterface(ABC):
    """Abstract camera interface"""
    
    @abstractmethod
    def open(self):
        pass
    
    @abstractmethod
    def read_frame(self) -> CameraFrame:
        pass
    
    @abstractmethod
    def release(self):
        pass

class OpenCVCamera(CameraInterface):
    """OpenCV camera implementation"""
    
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
    
    def open(self):
        """Open camera"""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {self.camera_id}")
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Warm up camera
        for _ in range(5):
            self.cap.read()
    
    def read_frame(self) -> CameraFrame:
        """Read a frame from camera"""
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Camera not opened")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Cannot read frame from camera")
        
        return CameraFrame(
            frame=frame,
            timestamp=time.time()
        )
    
    def release(self):
        """Release camera"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def __del__(self):
        self.release()
