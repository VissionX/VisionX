# Abserny - Object Detection for the Visually Impaired

A voice-activated object detection application designed to help visually impaired users understand their surroundings using artificial intelligence and speech feedback.

## Features

- **Voice Activation**: Say "start", "detect", "see", or "look" to trigger object detection
- **Offline Operation**: Uses Vosk for offline speech recognition and pyttsx3 for text-to-speech
- **Real-time Detection**: YOLOv8 for fast, accurate object detection
- **Natural Descriptions**: Converts detections into natural language descriptions
- **Accessible UI**: Clean KivyMD interface designed for accessibility

## Architecture

```
abserny/
├─ app/                     # UI entry point
│  └─ main.py              # KivyMD application
├─ orchestrator/            # Main coordination logic
│  └─ supervisor.py        # Orchestrates all services
├─ domain/                  # Business logic
│  ├─ entities.py          # Data models
│  └─ usecases.py          # Use cases
├─ services/                # External service wrappers
│  ├─ camera.py            # Camera interface
│  ├─ vision.py            # YOLO wrapper
│  ├─ audio.py             # Text-to-speech
│  └─ speech_recognition.py # Vosk wrapper
├─ infra/                   # Infrastructure
│  └─ config.py            # Configuration
└─ requirements.txt
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Vosk Model

Download a Vosk model for your language:
- English: [Offical Link](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
- Extract to a `model` folder in the project root

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 model
```

### 3. YOLO Model

The YOLOv8 nano model will be automatically downloaded on first run.

## Usage

### Run the Application

```bash
python app/main.py
```

### How It Works

1. The app starts listening for voice commands
2. Say "start" or another trigger word
3. The camera captures a frame
4. YOLO detects objects in the frame
5. The app speaks a natural description of what it sees
6. Returns to listening mode

### Trigger Words

- "start"
- "detect"
- "see"
- "look"
- "scan"

## Configuration

Edit `infra/config.py` to customize:

- Camera settings
- YOLO model and confidence threshold
- Trigger words
- Detection cooldown period
- TTS settings

## Example Output

**User says**: "start"

**App responds**: "Detecting... I see a person, a laptop, and 2 cups"

## Requirements

- Python 3.8+
- Webcam
- Microphone
- Speakers/headphones

## Troubleshooting

### No audio output
- Check that pyttsx3 is properly installed
- Try: `python -c "import pyttsx3; pyttsx3.init()"`

### Speech recognition not working
- Verify Vosk model is in the `model` folder
- Check microphone permissions
- Test microphone: `python -m sounddevice`

### Camera not found
- Check camera is connected and not in use
- Try changing `CAMERA_ID` in config (0, 1, 2, etc.)

### YOLO model not loading
- Ensure internet connection for first download
- Manually download from: [Direct Link](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt)

## Future Enhancements

- Distance estimation
- Directional information (left/right/center)
- Hazard detection (stairs, obstacles)
- Object tracking across frames
- Custom object classes for indoor/outdoor environments
- Multi-language support
- Gesture control

## License

This project is intended for educational purposes as a graduation project.

## Credits

- YOLOv8: Ultralytics
- Vosk: Alpha Cephei
- KivyMD: KivyMD Team
