from camera.camera_inputs import CameraInput
from audio.v_trigger import VoiceTrigger
from vision.obj_detection import ObjectDetector
from audio.audio_fb import AudioFeedback


def main():
    print("Starting VisionX Assist...")
    
    camera = CameraInput()
    voice = VoiceTrigger()
    detector = ObjectDetector()
    feedback = AudioFeedback()
    
    print("Waiting for voice trigger...")
    if voice.wait_for_trigger():
        print("Voice detected, starting camera stream...")
        for frame in camera.start_stream():
            objects = detector.detect(frame)
            feedback.speak(objects)
    
    print("Application ended.")


if __name__ == "__main__":
    main()

