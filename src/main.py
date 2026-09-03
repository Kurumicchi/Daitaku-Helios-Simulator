import time
import cv2
import mediapipe as mp
from poses import is_gyaru_peace

from audio import play_sound


MODEL_PATH = "models/hand_landmarker.task"



def main():
    last_trigger_time = 0
    trigger_cooldown = 1.5

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Could not open webcam.")
        return

    # Configure MediaPipe Hand Landmarker
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    RunningMode = mp.tasks.vision.RunningMode

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    with HandLandmarker.create_from_options(options) as landmarker:

        start_time = time.monotonic()

        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read webcam frame.")
                break

            # Flip image
            frame = cv2.flip(frame, 1)

            # Convert to RGB.
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to MediaPipe image
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame,
            )

            # Miliseconds timestamp
            timestamp_ms = int(
                (time.monotonic() - start_time) * 1000
            )

            # Detect hands
            result = landmarker.detect_for_video(
                mp_image,
                timestamp_ms,
            )

            # Draw detected hands
            if result.hand_landmarks:
                for hand in result.hand_landmarks:
                    draw_hand(frame, hand)

                if is_gyaru_peace(result.hand_landmarks):
                    print("GYARU PEACE DETECTED!")

                    current_time = time.monotonic()
                    if current_time - last_trigger_time >= trigger_cooldown:
                        play_sound("assets/audio/weiii.mp3")
                        last_trigger_time = current_time

                else:
                    print("NO GYARU PEACE")


            cv2.imshow("Daitaku Helios Simulator", frame)

            # Q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


def draw_hand(frame, landmarks):
    """Draw the 21 hand landmarks and their connections."""

    height, width, _ = frame.shape

    # Convert normalized coordinates to pixel coordinates.
    points = []

    for landmark in landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        points.append((x, y))

        # Draw landmark point.
        cv2.circle(
            frame,
            (x, y),
            5,
            (0, 255, 0),
            -1,
        )

    # MediaPipe's hand connections.
    connections = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),

        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),

        (5, 9),
        (9, 10),
        (10, 11),
        (11, 12),

        (9, 13),
        (13, 14),
        (14, 15),
        (15, 16),

        (13, 17),
        (17, 18),
        (18, 19),
        (19, 20),

        (0, 17),
    ]

    for start, end in connections:
        cv2.line(
            frame,
            points[start],
            points[end],
            (255, 0, 0),
            2,
        )


if __name__ == "__main__":
    main()