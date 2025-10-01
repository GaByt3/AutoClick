import sys
import json
import os
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QTabWidget, QMessageBox, QCheckBox,
    QHBoxLayout, QComboBox, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QColor, QIcon
from styles import *
import keyboard
from clicker import AutoClicker
from pynput import mouse

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "start_key": "f6",
        "pause_key": "f7",
        "delay": 0.5,
        "clicks_per_loop": 1,
        "button": "left"
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

class KeyCaptureThread(QThread):
    key_captured = pyqtSignal(str)

    def run(self):
        pressed_keys = set()
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                pressed_keys.add(event.name)
            elif event.event_type == keyboard.KEY_UP:
                combo = '+'.join(sorted(pressed_keys))
                if combo:
                    self.key_captured.emit(combo)
                    return

class MainTab(QWidget):
    def __init__(self, clicker, config):
        super().__init__()
        self.clicker = clicker
        self.config = config
        self.is_running = False

        layout = QVBoxLayout()
        layout.addStretch(10)  # centraliza Start/Status/Hotkeys

        # Bloco Start/Status/Hotkeys
        top_block = QVBoxLayout()

        self.toggle_button = QPushButton("Start")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(3, 3)
        self.toggle_button.setGraphicsEffect(shadow)
        self.toggle_button.setStyleSheet(toggle_button_style_start)
        self.toggle_button.setFixedSize(180, 60)
        self.toggle_button.clicked.connect(self.toggle_clicking)
        top_block.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        top_block.addSpacing(10)

        self.status_label = QLabel("Status: Paused")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px;")
        top_block.addWidget(self.status_label, alignment=Qt.AlignCenter)
        top_block.addSpacing(5)

        self.hotkey_label = QLabel(
            f"Start: {self.config['start_key'].title()} | Stop: {self.config['pause_key'].title()}"
        )
        self.hotkey_label.setAlignment(Qt.AlignCenter)
        self.hotkey_label.setStyleSheet("font-size: 12px; color: gray;")
        top_block.addWidget(self.hotkey_label, alignment=Qt.AlignCenter)

        layout.addLayout(top_block)
        layout.addStretch(10)  # empurra o bloco Mouse Button para baixo

        # Bloco Mouse Button + Click Type + Coordenadas
        mouse_layout = QHBoxLayout()
        mouse_layout.addWidget(QLabel("Mouse Button:"))
        self.button_selector = QComboBox()
        self.button_selector.addItems(["Left", "Right"])
        self.button_selector.setCurrentText(self.config.get("button", "Left").title())
        self.button_selector.setFixedHeight(28)
        self.button_selector.currentTextChanged.connect(self.change_mouse_button)
        mouse_layout.addWidget(self.button_selector)
        layout.addLayout(mouse_layout)
        layout.addSpacing(5)

        click_type_layout = QHBoxLayout()
        click_type_layout.addWidget(QLabel("Click Type:"))
        self.click_type_selector = QComboBox()
        self.click_type_selector.addItems(["Current location", "Pick location"])
        self.click_type_selector.currentTextChanged.connect(self.change_click_type)
        click_type_layout.addWidget(self.click_type_selector)
        layout.addLayout(click_type_layout)
        layout.addSpacing(5)

        coord_layout = QHBoxLayout()

        # Pega a geometria virtual (todos os monitores)
        screen = QApplication.primaryScreen()
        geometry = screen.virtualGeometry()

        self.x_input = QSpinBox()
        self.x_input.setRange(geometry.x(), geometry.x() + geometry.width())
        self.x_input.setValue(0)
        self.x_input.valueChanged.connect(self.update_position)

        self.y_input = QSpinBox()
        self.y_input.setRange(geometry.y(), geometry.y() + geometry.height())
        self.y_input.setValue(0)
        self.y_input.valueChanged.connect(self.update_position)

        coord_layout.addWidget(QLabel("X:"))
        coord_layout.addWidget(self.x_input)
        coord_layout.addWidget(QLabel("Y:"))
        coord_layout.addWidget(self.y_input)

        self.select_pos_button = QPushButton("Select on Screen")
        self.select_pos_button.clicked.connect(self.capture_position)
        coord_layout.addWidget(self.select_pos_button)

        layout.addLayout(coord_layout)

        self.change_click_type(self.click_type_selector.currentText())
        layout.addStretch(1)
        self.setLayout(layout)

    def toggle_clicking(self):
        if self.is_running:
            self.clicker.stop()
            self.is_running = False
            self.toggle_button.setText("Start")
            self.toggle_button.setStyleSheet(toggle_button_style_start)
            self.status_label.setText("Status: Paused")
        else:
            self.status_label.setText("Status: Starting in 1s...")
            QTimer.singleShot(1000, self.start_after_delay)

    def start_after_delay(self):
        self.clicker.start()
        self.is_running = True
        self.toggle_button.setText("Stop")
        self.toggle_button.setStyleSheet(toggle_button_style_stop)
        self.status_label.setText("Status: Running")

    def start_clicking(self):
        if not self.is_running:
            self.status_label.setText("Status: Starting in 1s...")
            threading.Timer(1.0, self.start_after_delay).start()

    def pause_clicking(self):
        if self.is_running:
            self.toggle_clicking()

    def change_mouse_button(self, text):
        self.clicker.button = text.lower()
        self.config["button"] = text.lower()
        save_config(self.config)

    def change_click_type(self, text):
        if text == "Current location":
            self.clicker.use_position = False
            self.x_input.setDisabled(True)
            self.y_input.setDisabled(True)
            self.select_pos_button.setDisabled(True)
            self.update_disabled_style()
        else:
            self.clicker.use_position = True
            self.x_input.setDisabled(False)
            self.y_input.setDisabled(False)
            self.select_pos_button.setDisabled(False)
            self.x_input.setStyleSheet("")
            self.y_input.setStyleSheet("")
            self.select_pos_button.setStyleSheet("")

    def update_position(self):
        self.clicker.position = (self.x_input.value(), self.y_input.value())

    def capture_position(self):
        self.status_label.setText("Click anywhere on the screen...")
        def on_click(x, y, button, pressed):
            if pressed:
                self.x_input.setValue(x)
                self.y_input.setValue(y)
                self.update_position()
                self.status_label.setText("Status: Ready")
                return False
        listener = mouse.Listener(on_click=on_click)
        listener.start()

    def update_disabled_style(self):
        if self.x_input.isEnabled():
            return
        is_dark = getattr(self.window(), "is_dark", True)
        disabled_bg = "#2a2a2a" if is_dark else "#e0e0e0"
        disabled_text = "#7a7a7a"
        self.x_input.setStyleSheet(f"background-color: {disabled_bg}; color: {disabled_text};")
        self.y_input.setStyleSheet(f"background-color: {disabled_bg}; color: {disabled_text};")
        self.select_pos_button.setStyleSheet(f"background-color: {disabled_bg}; color: {disabled_text};")

class ConfigTab(QWidget):
    def __init__(self, clicker, config, main_tab):
        super().__init__()
        self.clicker = clicker
        self.config = config
        self.main_tab = main_tab

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Keyboard Shortcuts", objectName="section_label"))

        hotkeys_form = QFormLayout()
        hotkeys_form.setVerticalSpacing(10)

        self.start_key_input = QLineEdit(self.config["start_key"].title())
        self.start_key_input.setReadOnly(True)
        self.start_key_button = QPushButton("Set start hotkey")
        self.start_key_button.clicked.connect(lambda: self.capture_key("start"))
        hotkeys_form.addRow("Start Hotkey:", self.start_key_input)
        hotkeys_form.addRow("", self.start_key_button)

        self.pause_key_input = QLineEdit(self.config["pause_key"].title())
        self.pause_key_input.setReadOnly(True)
        self.pause_key_button = QPushButton("Set stop hotkey")
        self.pause_key_button.clicked.connect(lambda: self.capture_key("pause"))
        hotkeys_form.addRow("Stop Hotkey:", self.pause_key_input)
        hotkeys_form.addRow("", self.pause_key_button)

        layout.addLayout(hotkeys_form)
        layout.addSpacing(20)

        layout.addWidget(QLabel("Click Options", objectName="section_label"))

        settings_form = QFormLayout()
        settings_form.setVerticalSpacing(10)

        self.delay_input = QDoubleSpinBox()
        self.delay_input.setValue(self.config.get("delay", 0.5))
        self.delay_input.setSingleStep(0.1)
        self.delay_input.valueChanged.connect(self.update_delay)
        settings_form.addRow("Delay between clicks (s):", self.delay_input)

        self.clicks_input = QSpinBox()
        self.clicks_input.setValue(self.config.get("clicks_per_loop", 1))
        self.clicks_input.setMinimum(1)
        self.clicks_input.valueChanged.connect(self.update_clicks)
        settings_form.addRow("Number of clicks per loop:", self.clicks_input)

        layout.addLayout(settings_form)
        self.setLayout(layout)

    def capture_key(self, key_type):
        if key_type == "start":
            self.start_key_input.setText("Press a key...")
        else:
            self.pause_key_input.setText("Press a key...")

        self.start_key_button.setEnabled(False)
        self.pause_key_button.setEnabled(False)

        self.key_thread = KeyCaptureThread()
        self.key_thread.key_captured.connect(lambda key: self.key_selected(key_type, key))
        self.key_thread.start()

    def key_selected(self, key_type, key):
        other_key = self.config["pause_key"] if key_type == "start" else self.config["start_key"]
        if key.lower() == other_key.lower():
            QMessageBox.warning(self, "Hotkey Conflict", "Start and Stop hotkeys cannot be the same!")
            if key_type == "start":
                self.start_key_input.setText(self.config["start_key"].title())
            else:
                self.pause_key_input.setText(self.config["pause_key"].title())
            self.start_key_button.setEnabled(True)
            self.pause_key_button.setEnabled(True)
            return

        if key_type == "start":
            self.start_key_input.setText(key.title())
            self.config["start_key"] = key
        else:
            self.pause_key_input.setText(key.title())
            self.config["pause_key"] = key

        self.start_key_button.setEnabled(True)
        self.pause_key_button.setEnabled(True)
        self.update_hotkeys()

    def update_hotkeys(self):
        keyboard.clear_all_hotkeys()
        keyboard.add_hotkey(self.config["start_key"], self.main_tab.start_clicking)
        keyboard.add_hotkey(self.config["pause_key"], self.main_tab.pause_clicking)
        save_config(self.config)
        self.main_tab.hotkey_label.setText(
            f"Start: {self.config['start_key'].title()} | Stop: {self.config['pause_key'].title()}"
        )

    def update_delay(self):
        self.clicker.delay = self.delay_input.value()
        self.config["delay"] = self.delay_input.value()
        save_config(self.config)

    def update_clicks(self):
        self.clicker.clicks_per_loop = self.clicks_input.value()
        self.config["clicks_per_loop"] = self.clicks_input.value()
        save_config(self.config)

class AutoClickUI(QWidget):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(__file__)  
        icon_path = os.path.join(base_dir, "assets", "click_icon.ico")

        self.setWindowTitle("AutoTap")
        self.setWindowIcon(QIcon(icon_path))
        self.resize(400, 420)

        self.is_dark = True
        self.setStyleSheet(dark_style + toggle_style)

        self.config = load_config()
        self.clicker = AutoClicker(
            delay=self.config["delay"],
            clicks_per_loop=self.config["clicks_per_loop"],
            button=self.config.get("button", "left")
        )

        self.theme_switch = QCheckBox("Dark Mode")
        self.theme_switch.setChecked(True)
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        self.theme_switch.setFixedWidth(120)

        self.tabs = QTabWidget()
        self.main_tab = MainTab(self.clicker, self.config)
        self.config_tab = ConfigTab(self.clicker, self.config, self.main_tab)
        self.tabs.addTab(self.main_tab, "Home")
        self.tabs.addTab(self.config_tab, "Settings")
        self.tabs.setCornerWidget(self.theme_switch, Qt.TopRightCorner)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        keyboard.add_hotkey(self.config["start_key"], self.main_tab.start_clicking)
        keyboard.add_hotkey(self.config["pause_key"], self.main_tab.pause_clicking)

    def toggle_theme(self, state):
        if state == Qt.Checked:
            self.setStyleSheet(dark_style + toggle_style)
            self.theme_switch.setText("Dark Mode")
            self.is_dark = True
        else:
            self.setStyleSheet(light_style + toggle_style)
            self.theme_switch.setText("Light Mode")
            self.is_dark = False

        self.main_tab.update_disabled_style()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClickUI()
    window.show()
    sys.exit(app.exec_())
