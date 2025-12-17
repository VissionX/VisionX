class Config:
    def __init__(self):
        self.CAMERA_ID = 0
        self.CAMERA_WIDTH = 640
        self.CAMERA_HEIGHT = 480
        self.YOLO_MODEL = 'yolov8n.pt'
        self.CONFIDENCE_THRESHOLD = 0.5
        self.VOSK_MODEL_PATH = 'model'
        self.SAMPLE_RATE = 16000
        self.TRIGGER_WORDS = ['start', 'detect', 'see', 'look', 'scan']
        self.TTS_RATE = 150
        self.TTS_VOLUME = 1.0
        self.DETECTION_COOLDOWN = 3.0
