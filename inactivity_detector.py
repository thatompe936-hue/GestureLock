import ctypes
import time


class InactivityDetector:

    def __init__(self):
        self.last_input_time = time.time()

    def get_idle_seconds(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)
            ]

        info = LASTINPUTINFO()
        info.cbSize = ctypes.sizeof(LASTINPUTINFO)

        ctypes.windll.user32.GetLastInputInfo(
            ctypes.byref(info)
        )

        tick_count = ctypes.windll.kernel32.GetTickCount()
        idle_time = tick_count - info.dwTime

        return idle_time / 1000.0

    def is_idle(self, seconds):
        return self.get_idle_seconds() >= seconds