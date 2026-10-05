import threading
import time
import tkinter as tk
from tkinter import ttk

from pynput import keyboard, mouse

mouse_ctl = mouse.Controller()

VK_Z = 90
VK_X = 88

INTERVAL_SECONDS = 90  # 1 минута 30 секунд


class AntiAFK:
    def __init__(self, root):
        self.root = root
        root.title("АнтиАФК")
        root.geometry("340x220")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        self.running = False
        self.seconds_left = INTERVAL_SECONDS

        self.status = tk.StringVar(value="Выключен")
        self.timer_text = tk.StringVar(value="")

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Имитация действия каждые 1:30").grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )

        ttk.Button(frame, text="Включить / Выключить", command=self.toggle).grid(
            row=1, column=0, columnspan=2, pady=10, sticky="ew"
        )

        ttk.Label(frame, textvariable=self.status, font=("Segoe UI", 11, "bold")).grid(
            row=2, column=0, columnspan=2
        )
        ttk.Label(frame, textvariable=self.timer_text, foreground="gray").grid(
            row=3, column=0, columnspan=2, pady=(4, 0)
        )
        ttk.Label(frame, text="Z - вкл,  X - выкл,  Esc - авостоп", foreground="gray").grid(
            row=4, column=0, columnspan=2, pady=(12, 0)
        )

        threading.Thread(target=self.loop, daemon=True).start()
        keyboard.Listener(on_press=self.on_press).start()
        self.refresh()

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.seconds_left = INTERVAL_SECONDS

    def on_press(self, key):
        vk = getattr(key, "vk", None)
        if vk == VK_Z:
            self.running = True
            self.seconds_left = INTERVAL_SECONDS
        elif vk == VK_X:
            self.running = False
        elif key == keyboard.Key.esc:
            self.running = False

    def jiggle(self):
        mouse_ctl.move(1, 0)
        time.sleep(0.05)
        mouse_ctl.move(-1, 0)

    def loop(self):
        while True:
            if self.running:
                if self.seconds_left <= 0:
                    self.jiggle()
                    self.seconds_left = INTERVAL_SECONDS
                else:
                    self.seconds_left -= 1
            time.sleep(1)

    def refresh(self):
        self.status.set("ВКЛЮЧЕН" if self.running else "Выключен")
        if self.running:
            m, s = divmod(self.seconds_left, 60)
            self.timer_text.set(f"До следующего действия: {m}:{s:02d}")
        else:
            self.timer_text.set("")
        self.root.after(1000, self.refresh)


if __name__ == "__main__":
    root = tk.Tk()
    AntiAFK(root)
    root.mainloop()
