import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

class VoiceTrigger:
    def __init__(self, model_path="models/vosk-model-small-ar-0.22", trigger_word="start"):
        self.model_path = model_path
        self.trigger_word = trigger_word
        self.q = queue.Queue()

        print(f"Loading speech model from: {model_path}")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def _callback(self, indata, frames, time, status):
        """Callback function for sounddevice stream"""
        if status:
            print(f"[Audio Warning] {status}")
        self.q.put(bytes(indata))

    def listen_for_command(self):
        """Listen to the microphone and return recognized text"""
        print("Listening for voice command...")

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback
        ):
            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"[Recognized]: {text}")
                        return text

    def check_trigger(self):
        """Check if the trigger word is spoken"""
        command = self.listen_for_command()
        if command and self.trigger_word in command:
            print("Trigger word detected!")
            return True
        return False

