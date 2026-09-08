import cv2


def draw_menu(frame):
    cv2.putText(
        frame,
        "PRESS Z TO START",
        (150, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        3,
    )