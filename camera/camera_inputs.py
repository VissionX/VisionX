import cv2

def main():
    print("Opening camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to open camera")
        return

    print("Camera opened successfully.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to read frame")
            break

        cv2.imshow("Camera Test", frame)

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

