import threading
import time
import pyautogui

class AutoClicker:
    def __init__(self, delay=0.5, clicks_per_loop=1, button="left", use_position=False, position=(0,0)):
        self.delay = delay
        self.clicks_per_loop = clicks_per_loop
        self.running = False
        self.thread = None
        self.button = button.lower() if button.lower() in ("left", "middle", "right") else "left"
        self.use_position = use_position  # True se for clicar em posição fixa
        self.position = position          # coordenadas (x, y) se usar posição fixa

    def click_loop(self):
        while self.running:
            for _ in range(self.clicks_per_loop):
                if self.use_position:
                    pyautogui.click(x=self.position[0], y=self.position[1], button=self.button)
                else:
                    pyautogui.click(button=self.button)
            time.sleep(self.delay)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.click_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
