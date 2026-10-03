import customtkinter as ctk
from config import load_settings, save_settings


class SettingsWindow:

    def __init__(self):
        self.settings = load_settings()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("GestureLock Settings")
        self.window.geometry("600x650")
        self.window.resizable(False, False)

        self.create_interface()

    def create_interface(self):

        title = ctk.CTkLabel(
            self.window,
            text="GESTURELOCK",
            font=("Arial", 32, "bold")
        )

        title.pack(pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self.window,
            text="Security & Lock Settings",
            font=("Arial", 16)
        )

        subtitle.pack(pady=(0, 30))

        auto_frame = ctk.CTkFrame(self.window)

        auto_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        auto_label = ctk.CTkLabel(
            auto_frame,
            text="Automatic Lock",
            font=("Arial", 17, "bold")
        )

        auto_label.pack(
            side="left",
            padx=20,
            pady=20
        )

        self.auto_switch = ctk.CTkSwitch(
            auto_frame,
            text="",
        )

        self.auto_switch.pack(
            side="right",
            padx=20
        )

        if self.settings["auto_lock_enabled"]:
            self.auto_switch.select()

        timeout_label = ctk.CTkLabel(
            self.window,
            text="Lock after inactivity",
            font=("Arial", 16)
        )

        timeout_label.pack(
            anchor="w",
            padx=45,
            pady=(25, 5)
        )

        self.timeout_entry = ctk.CTkEntry(
            self.window,
            width=510,
            height=40,
            placeholder_text="Seconds"
        )

        self.timeout_entry.pack(padx=40)

        self.timeout_entry.insert(
            0,
            str(self.settings["auto_lock_seconds"])
        )

        hold_label = ctk.CTkLabel(
            self.window,
            text="Gesture hold time",
            font=("Arial", 16)
        )

        hold_label.pack(
            anchor="w",
            padx=45,
            pady=(25, 5)
        )

        self.hold_entry = ctk.CTkEntry(
            self.window,
            width=510,
            height=40,
            placeholder_text="Seconds"
        )

        self.hold_entry.pack(padx=40)

        self.hold_entry.insert(
            0,
            str(self.settings["gesture_stable_time"])
        )

        sequence_frame = ctk.CTkFrame(self.window)

        sequence_frame.pack(
            fill="x",
            padx=40,
            pady=30
        )

        sequence_title = ctk.CTkLabel(
            sequence_frame,
            text="Current Gesture Password",
            font=("Arial", 16, "bold")
        )

        sequence_title.pack(pady=(15, 5))

        sequence_text = ctk.CTkLabel(
            sequence_frame,
            text="✌️   ✊️   🖕   🖐",
            font=("Arial", 30)
        )

        sequence_text.pack(pady=(5, 15))

        self.status_label = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 14)
        )

        self.status_label.pack(pady=5)

        save_button = ctk.CTkButton(
            self.window,
            text="SAVE SETTINGS",
            width=510,
            height=45,
            font=("Arial", 16, "bold"),
            command=self.save
        )

        save_button.pack(pady=10)

    def save(self):

        try:
            timeout = int(self.timeout_entry.get())
            hold_time = float(self.hold_entry.get())

            if timeout < 5:
                self.status_label.configure(
                    text="Lock timeout must be at least 5 seconds."
                )
                return

            if hold_time < 0.1:
                self.status_label.configure(
                    text="Gesture hold time must be at least 0.1 seconds."
                )
                return

            self.settings["auto_lock_enabled"] = bool(
                self.auto_switch.get()
            )

            self.settings["auto_lock_seconds"] = timeout
            self.settings["gesture_stable_time"] = hold_time

            save_settings(self.settings)

            self.status_label.configure(
                text="Settings saved successfully."
            )

        except ValueError:

            self.status_label.configure(
                text="Please enter valid numbers."
            )

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = SettingsWindow()
    app.run()