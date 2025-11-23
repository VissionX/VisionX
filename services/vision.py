from ultralytics import YOLO
from domain.entities import CameraFrame, Detection
import time

class YOLOVisionService:
    """YOLO-based object detection service"""
    
    def __init__(self, model_name='yolov8n.pt', confidence_threshold=0.5):
        """
        Initialize YOLO model
        
        Args:
            model_name: YOLO model to use (yolov8n.pt is fastest)
            confidence_threshold: Minimum confidence for detections
        """
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold
    
    def detect_objects(self, frame) -> CameraFrame:
        """
        Detect objects in frame
        
        Args:
            frame: Camera frame or numpy array
            
        Returns:
            CameraFrame with detections
        """
        if isinstance(frame, CameraFrame):
            img = frame.frame
            timestamp = frame.timestamp
        else:
            img = frame
            timestamp = time.time()
        
        # Run detection
        results = self.model(img, verbose=False)[0]
        
        # Extract detections
        detections = []
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf >= self.confidence_threshold:
                cls_id = int(box.cls[0])
                class_name = results.names[cls_id]
                bbox = box.xyxy[0].cpu().numpy().tolist()
                
                detections.append(Detection(
                    class_name=class_name,
                    confidence=conf,
                    bbox=tuple(bbox)
                ))
        
        return CameraFrame(
            frame=img,
            timestamp=timestamp,
            detections=detections
        )
    
    def warm_up(self):
        """Warm up model with dummy inference"""
        import numpy as np
        dummy = np.zeros((640, 480, 3), dtype=np.uint8)
        self.detect_objects(dummy)
