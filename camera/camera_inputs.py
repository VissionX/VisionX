class CameraInput:
    def start_stream(self):

        for i in range(3):
            yield f"frame_{i}"

