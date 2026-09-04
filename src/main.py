import time
import cv2
import mediapipe as mp
from poses import is_gyaru_peace, is_helios_peace

from audio import play_sound


HAND_MODEL_PATH = "models/hand_landmarker.task"
POSE_MODEL_PATH = "models/pose_landmarker.task"



def main():
    last_trigger_time = 0
    trigger_cooldown = 1.5

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Could not open webcam.")
        return

    # Initialize MediaPipe Hand Landmarker
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    RunningMode = mp.tasks.vision.RunningMode

    hand_options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=HAND_MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    pose_options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=POSE_MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    with (
        HandLandmarker.create_from_options(hand_options) as landmarker,
        PoseLandmarker.create_from_options(pose_options) as pose_landmarker
    ):

        start_time = time.monotonic()

        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read webcam frame.")
                break

            # Flip image
            # frame = cv2.flip(frame, 1)

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

            # Detect hands and upperbody pose
            hand_result = landmarker.detect_for_video(
                mp_image,
                timestamp_ms,
            )
            pose_result = pose_landmarker.detect_for_video(
                mp_image,
                timestamp_ms
            )

            # Draw detected hands
            if hand_result.hand_landmarks:

                # Draw all detected hands
                for hand in hand_result.hand_landmarks:
                    draw_hand(frame, hand)

                # --------------------------------
                # Uses both hands
                # --------------------------------

                if is_gyaru_peace(hand_result.hand_landmarks):
                    print("GYARU PEACE DETECTED!")

                    current_time = time.monotonic()
                    if current_time - last_trigger_time >= trigger_cooldown:
                        play_sound("assets/audio/weiii.mp3")
                        last_trigger_time = current_time

                else:
                    # --------------------------------
                    # Right hand only
                    # --------------------------------

                    helios_detected = False

                    for hand, handedness in zip(
                        hand_result.hand_landmarks,
                        hand_result.handedness,
                    ):
                        # print(handedness[0].category_name)
                        if handedness[0].category_name == "Right":

                            if (
                                pose_result.pose_landmarks
                                and is_helios_peace(
                                    hand,
                                    pose_result.pose_landmarks[0],
                                )
                            ):
                                helios_detected = True
                                break

                    if helios_detected:
                        print("HELIOS PEACE DETECTED!")
                    else:
                        print("NO POSE")

            # Draw detected pose
            if pose_result.pose_landmarks:
                draw_upper_body(frame, pose_result.pose_landmarks[0])

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

def draw_upper_body(frame, landmarks):
    """Draw only shoulder, elbow, and wrist landmarks."""

    height, width, _ = frame.shape

    # Select landmarks for shoulders, elbows, and wrists
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    left_elbow = landmarks[13]
    right_elbow = landmarks[14]

    left_wrist = landmarks[15]
    right_wrist = landmarks[16]

    points = []

    selected_landmarks = [
        left_shoulder,
        left_elbow,
        left_wrist,
        right_shoulder,
        right_elbow,
        right_wrist,
    ]

    for landmark in selected_landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        points.append((x, y))

        cv2.circle(
            frame,
            (x, y),
            7,
            (0, 0, 255),
            -1,
        )

    # Left arm: shoulder → elbow → wrist
    cv2.line(
        frame,
        points[0],
        points[1],
        (0, 0, 255),
        3,
    )

    cv2.line(
        frame,
        points[1],
        points[2],
        (0, 0, 255),
        3,
    )

    # Right arm: shoulder → elbow → wrist
    cv2.line(
        frame,
        points[3],
        points[4],
        (0, 0, 255),
        3,
    )

    cv2.line(
        frame,
        points[4],
        points[5],
        (0, 0, 255),
        3,
    )

if __name__ == "__main__":
    main()