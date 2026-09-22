import cv2
import time

from uart import PicoUART
from vision import VisionSystem
from navigation import Navigator


# ==========================================
# SETTINGS
# ==========================================

SHOW_CAMERA = True

LOOP_DELAY = 0.03


# ==========================================
# INITIALIZE
# ==========================================

print("--------------------------------")
print("WRO 2026 FUTURE ENGINEERS")
print("TEAM 6001")
print("--------------------------------")


pico = PicoUART(
    port="/dev/ttyACM0",
    baudrate=115200
)

if not pico.connect():

    print("Pico connection failed.")
    exit()


vision = VisionSystem()

navigator = Navigator()


# ==========================================
# START STATE
# ==========================================

pico.stop()
pico.center()

time.sleep(2)

print("[SYSTEM] Robot ready")


# ==========================================
# MAIN LOOP
# ==========================================

try:

    while True:

        # --------------------------
        # Camera processing
        # --------------------------

        vision_result = vision.process()

        # --------------------------
        # Navigation decision
        # --------------------------

        command = navigator.calculate(
            vision_result
        )

        drive = command["drive"]
        steering = command["steering"]
        state = command["state"]

        # --------------------------
        # Motor command
        # --------------------------

        if drive == "F":

            pico.forward()

        elif drive == "B":

            pico.backward()

        else:

            pico.stop()

        # --------------------------
        # Steering command
        # --------------------------

        if steering == "L":

            pico.left()

        elif steering == "R":

            pico.right()

        else:

            pico.center()

        # --------------------------
        # Debug
        # --------------------------

        print(
            f"STATE: {state:15} "
            f"DRIVE: {drive} "
            f"STEERING: {steering}"
        )

        # --------------------------
        # Camera window
        # --------------------------

        if SHOW_CAMERA:

            display = vision.draw_detection(
                vision_result
            )

            cv2.putText(
                display,
                f"STATE: {state}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "WRO 2026 - Team 6001",
                display
            )

            key = cv2.waitKey(1)

            if key == ord("q"):
                break

        time.sleep(LOOP_DELAY)


# ==========================================
# SAFE SHUTDOWN
# ==========================================

except KeyboardInterrupt:

    print("\n[SYSTEM] CTRL+C")


finally:

    print("[SYSTEM] STOPPING")

    pico.stop()
    pico.center()

    vision.close()
    pico.close()

    print("[SYSTEM] OFF")