import time
import pygame
import ctypes
import cv2
import customtkinter as ctk
from gesture_detector import GestureDetector
from lock_screen import LockScreen
from inactivity_detector import InactivityDetector
from config import load_settings
from settings_window import SettingsWindow


def is_manual_lock_pressed():
    user32 = ctypes.windll.user32

    ctrl = user32.GetAsyncKeyState(0x11) & 0x8000
    alt = user32.GetAsyncKeyState(0x12) & 0x8000
    l_key = user32.GetAsyncKeyState(0x4C) & 0x8000

    return ctrl and alt and l_key


def run_gesture_lock():
    settings = load_settings()

    detector = GestureDetector()
    lock_screen = LockScreen()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        detector.close()
        lock_screen.close()
        return False

    sequence = settings["unlock_sequence"]
    stable_time = settings["gesture_stable_time"]

    progress = 0
    current_gesture = None
    tracked_gesture = None
    gesture_start_time = 0
    waiting_for_change = False

    running = True
    unlocked = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        success, frame = camera.read()

        if not success:
            continue

        frame = cv2.flip(frame, 1)

        detected_gesture = detector.detect(frame)

        current_gesture = detected_gesture

        if detected_gesture is None:
            tracked_gesture = None
            gesture_start_time = 0
            waiting_for_change = False

        else:

            if waiting_for_change:

                if detected_gesture != tracked_gesture:
                    waiting_for_change = False
                    tracked_gesture = detected_gesture
                    gesture_start_time = time.time()

            else:

                if detected_gesture != tracked_gesture:
                    tracked_gesture = detected_gesture
                    gesture_start_time = time.time()

                elif time.time() - gesture_start_time >= stable_time:

                    if progress < len(sequence):

                        expected_gesture = sequence[progress]

                        if detected_gesture == expected_gesture:
                            progress += 1
                            waiting_for_change = True
                            gesture_start_time = 0

                            if progress >= len(sequence):
                                unlocked = True
                                break

        next_gesture = (
            sequence[progress]
            if progress < len(sequence)
            else None
        )

        lock_screen.draw(
            frame,
            progress,
            current_gesture,
            next_gesture
        )

    camera.release()
    detector.close()
    lock_screen.close()

    return unlocked


class GestureLockApp:

    def __init__(self):

        self.settings = load_settings()
        self.inactivity = InactivityDetector()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()

        self.window.title("GestureLock")
        self.window.geometry("650x600")
        self.window.resizable(False, False)

        self.create_interface()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self.update_status()

    def create_interface(self):

        title = ctk.CTkLabel(
            self.window,
            text="GESTURELOCK",
            font=("Arial", 36, "bold")
        )

        title.pack(pady=(40, 5))

        subtitle = ctk.CTkLabel(
            self.window,
            text="Gesture-Based PC Security",
            font=("Arial", 17)
        )

        subtitle.pack(pady=(0, 35))

        status_frame = ctk.CTkFrame(
            self.window,
            width=550,
            height=150
        )

        status_frame.pack(
            padx=40,
            fill="x"
        )

        status_title = ctk.CTkLabel(
            status_frame,
            text="SYSTEM STATUS",
            font=("Arial", 18, "bold")
        )

        status_title.pack(pady=(20, 5))

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="PROTECTED",
            font=("Arial", 25, "bold")
        )

        self.status_label.pack()

        self.timeout_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=("Arial", 15)
        )

        self.timeout_label.pack(pady=5)

        button_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=40,
            pady=35
        )

        lock_button = ctk.CTkButton(
            button_frame,
            text="LOCK NOW",
            height=55,
            font=("Arial", 18, "bold"),
            command=self.lock_now
        )

        lock_button.pack(
            fill="x",
            pady=8
        )

        settings_button = ctk.CTkButton(
            button_frame,
            text="SETTINGS",
            height=50,
            font=("Arial", 16, "bold"),
            command=self.open_settings
        )

        settings_button.pack(
            fill="x",
            pady=8
        )

        hotkey_label = ctk.CTkLabel(
            self.window,
            text="Quick Lock: Ctrl + Alt + L",
            font=("Arial", 14)
        )

        hotkey_label.pack(pady=10)

        gesture_label = ctk.CTkLabel(
            self.window,
            text="Unlock: ✌️  →  ✊️  →  🖕  →  🖐",
            font=("Arial", 18)
        )

        gesture_label.pack(pady=5)

    def update_status(self):

        self.settings = load_settings()

        enabled = self.settings["auto_lock_enabled"]
        timeout = self.settings["auto_lock_seconds"]

        if enabled:
            self.timeout_label.configure(
                text=f"Automatic Lock: ON  •  {timeout} seconds"
            )
        else:
            self.timeout_label.configure(
                text="Automatic Lock: OFF"
            )

        self.window.after(
            1000,
            self.update_status
        )

    def lock_now(self):

        self.window.withdraw()

        unlocked = run_gesture_lock()

        self.window.deiconify()

        if not unlocked:
            self.close()

    def open_settings(self):

        settings_window = SettingsWindow()

        settings_window.window.transient(
            self.window
        )

        settings_window.window.grab_set()

        settings_window.run()

    def check_inactivity(self):

        settings = load_settings()

        if settings["auto_lock_enabled"]:

            timeout = settings["auto_lock_seconds"]

            if self.inactivity.get_idle_seconds() >= timeout:

                self.lock_now()

        self.window.after(
            500,
            self.check_inactivity
        )

    def close(self):

        self.window.destroy()


def main():

    app = GestureLockApp()

    app.window.after(
        500,
        app.check_inactivity
    )

    app.window.mainloop()


if __name__ == "__main__":
    main()