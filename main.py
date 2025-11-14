# from camera.camera_inputs import CameraInput
from audio.v_trigger import VoiceTrigger
# from vision.obj_detection import ObjectDetector

def main():
    print("Starting VisionX voice system...")
    trigger = VoiceTrigger(trigger_word="start")

    if trigger.check_trigger():
        print("✅ Voice command recognized! (Start detected)")
        # later this will trigger the camera
    else:
        print("❌ No valid command detected.")

if __name__ == "__main__":
    main()

