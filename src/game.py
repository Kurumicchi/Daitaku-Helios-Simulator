import cv2
import numpy as np

GAME_WIDTH = 1280
GAME_HEIGHT = 720

# Define pose
POSES = {
    "helios_peace": "assets/img/Peace.png",
    "gyaru_peace": "assets/img/Gyaru.png"
}

class Game:
    def __init__(self):
        self.current_pose = "helios_peace"
        self.expected_image = None
        self.detected_pose = None
        self.success = False

        self.load_expected_image()

    # Load the expected pose image
    def load_expected_image(self):
        pose_path = POSES.get(self.current_pose)

        self.expected_image = cv2.imread(
            pose_path,
            cv2.IMREAD_UNCHANGED,
        )

        if self.expected_image is None:
            print(
                f"Could not load image: {pose_path}"
            )

    # Update the detected pose and check if it matches
    def update(self, detected_pose):
        self.detected_pose = detected_pose

        if self.detected_pose == self.current_pose:
            self.success = True
        else:
            self.success = False

    # Draw
    def draw(self, camera_frame):
        game_frame = np.zeros(
            (GAME_HEIGHT, GAME_WIDTH, 3),
            dtype=np.uint8
        )

        self.draw_camera(
            game_frame,
            camera_frame,
        )

        self.draw_expected_pose(game_frame)
        self.draw_ui(game_frame)

        return game_frame

    def draw_camera(self, game_frame, camera_frame):
        x = 40
        y = 100

        width = 560
        height = 420

        camera = cv2.resize(
            camera_frame,
            (width, height)
        )

        game_frame[
            y:y + height,
            x:x + width
        ] = camera
    
    def draw_ui(self, game_frame):

        cv2.putText(
            game_frame,
            "DAITAKU HELIOS SIMULATOR",
            (40, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            game_frame,
            f"Expected: {self.current_pose}",
            (800, 670),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            game_frame,
            f"Detected: {self.detected_pose}",
            (40, 670),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        if self.success:

            cv2.putText(
                game_frame,
                "SUCCESS!",
                (500, 705),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                3,
            )

    # Draw the expected pose image
    def draw_expected_pose(self, frame):
        image = self.expected_image

        if image is None:
            return

        width = 560
        height = 420

        image = cv2.resize(
            image,
            (width, height),
        )

        x = 680
        y = 100

        if image.shape[2] == 4:
            bgr = image[:, :, :3]
            alpha = image[:, :, 3] / 255.0

            for c in range(3):
                frame[
                    y:y + height,
                    x:x + width,
                    c
                ] = (
                    alpha * bgr[:, :, c]
                    + (1 - alpha) * frame[
                        y:y + height,
                        x:x + width,
                        c
                    ]
                ).astype("uint8")

        else:
            frame[
                y:y + height,
                x:x + width
            ] = image