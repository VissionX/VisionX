from typing import List
from domain.entities import CameraFrame, Detection

class ProcessFrameUseCase:
    """Process a camera frame and return detections"""
    
    def __init__(self, vision_service):
        self.vision_service = vision_service
    
    def execute(self, frame) -> CameraFrame:
        """Process frame and return detections"""
        return self.vision_service.detect_objects(frame)

class GenerateDescriptionUseCase:
    """Generate natural language description from detections"""
    
    def execute(self, detections: List[Detection]) -> str:
        """Convert detections to natural speech"""
        if not detections:
            return "I don't see anything clearly"
        
        # Group by class name
        obj_counts = {}
        for det in detections:
            if det.confidence > 0.5:  # Filter low confidence
                obj_counts[det.class_name] = obj_counts.get(det.class_name, 0) + 1
        
        if not obj_counts:
            return "I don't see anything clearly"
        
        # Build description
        if len(obj_counts) == 1:
            obj, count = list(obj_counts.items())[0]
            if count == 1:
                return f"I see a {obj}"
            else:
                return f"I see {count} {obj}s"
        else:
            items = []
            for obj, count in list(obj_counts.items())[:5]:  # Limit to 5 objects
                if count == 1:
                    items.append(f"a {obj}")
                else:
                    items.append(f"{count} {obj}s")
            
            if len(items) == 2:
                return f"I see {items[0]} and {items[1]}"
            else:
                return f"I see {', '.join(items[:-1])}, and {items[-1]}"
