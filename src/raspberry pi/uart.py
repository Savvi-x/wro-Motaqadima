import serial
import time


class PicoUART:

    def __init__(self, port="/dev/ttyACM0", baudrate=115200):

        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self):

        try:
            self.ser = serial.Serial(
                self.port,
                self.baudrate,
                timeout=0.05
            )

            time.sleep(2)

            print(f"[UART] Connected to Pico on {self.port}")

            return True

        except Exception as error:

            print("[UART ERROR]", error)

            return False

    def send(self, command):

        if self.ser is None:
            return

        try:
            self.ser.write(command.encode())
            self.ser.flush()

        except Exception as error:
            print("[UART SEND ERROR]", error)

    def forward(self):
        self.send("F")

    def backward(self):
        self.send("B")

    def stop(self):
        self.send("S")

    def left(self):
        self.send("L")

    def right(self):
        self.send("R")

    def center(self):
        self.send("C")

    def close(self):

        if self.ser is not None:

            self.stop()
            self.center()

            self.ser.close()

            print("[UART] Closed")