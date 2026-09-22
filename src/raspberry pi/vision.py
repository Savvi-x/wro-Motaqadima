import cv2
import numpy as np

from picamera2 import Picamera2


class VisionSystem:

    def __init__(self):

        self.camera = Picamera2()

        config = self.camera.create_preview_configuration(
            main={
                "format": "RGB888",
                "size": (640, 480)
            }
        )

        self.camera.configure(config)
        self.camera.start()

        self.frame_width = 640
        self.frame_height = 480

        print("[VISION] Camera started")

    def detect_color(self, frame, lower, upper):

        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        mask = cv2.inRange(
            hsv,
            np.array(lower),
            np.array(upper)
        )

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)

        area = cv2.contourArea(largest)

        if area < 700:
            return None

        x, y, w, h = cv2.boundingRect(largest)

        center_x = x + w // 2
        center_y = y + h // 2

        return {
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "center_x": center_x,
            "center_y": center_y,
            "area": area
        }

    def process(self):

        frame = self.camera.capture_array()

        # =========================
        # RED
        # =========================

        # Red wraps around HSV,
        # therefore two ranges are used.

        red1 = self.detect_color(
            frame,
            (0, 100, 70),
            (10, 255, 255)
        )

        red2 = self.detect_color(
            frame,
            (170, 100, 70),
            (180, 255, 255)
        )

        red = red1

        if red2 is not None:

            if red is None or red2["area"] > red["area"]:
                red = red2

        # =========================
        # GREEN
        # =========================

        green = self.detect_color(
            frame,
            (35, 70, 50),
            (90, 255, 255)
        )

        result = {
            "red": red,
            "green": green,
            "frame": frame
        }

        return result

    def draw_detection(self, result):

        frame = result["frame"]

        if result["red"] is not None:

            r = result["red"]

            cv2.rectangle(
                frame,
                (r["x"], r["y"]),
                (r["x"] + r["w"], r["y"] + r["h"]),
                (255, 0, 0),
                3
            )

            cv2.putText(
                frame,
                "RED",
                (r["x"], r["y"] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

        if result["green"] is not None:

            g = result["green"]

            cv2.rectangle(
                frame,
                (g["x"], g["y"]),
                (g["x"] + g["w"], g["y"] + g["h"]),
                (0, 255, 0),
                3
            )

            cv2.putText(
                frame,
                "GREEN",
                (g["x"], g["y"] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        return frame

    def close(self):

        self.camera.stop()
        cv2.destroyAllWindows()

        print("[VISION] Camera stopped")