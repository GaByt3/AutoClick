# styles.py

dark_style = """
QWidget {
    background-color: #121212;
    color: #ffffff;
    font-family: Arial;
    font-size: 14px;
}
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #1e1e1e;
    border: 1px solid #333;
    padding: 4px;
    border-radius: 4px;
    color: #ffffff;
}
QPushButton {
    background-color: #2e2e2e;
    border: 1px solid #444;
    padding: 6px;
    border-radius: 4px;
    color: #ffffff;
}
QPushButton:hover {
    background-color: #444444;
}
QTabWidget::pane {
    border: 1px solid #444;
}
QTabBar::tab {
    background: #1e1e1e;
    padding: 6px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #2e2e2e;
}
QLabel#section_label {
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 10px;
}
"""

light_style = """
QWidget {
    background-color: #f0f0f0;
    color: #000000;
    font-family: Arial;
    font-size: 14px;
}
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #ccc;
    padding: 4px;
    border-radius: 4px;
    color: #000000;
}
QPushButton {
    background-color: #e0e0e0;
    border: 1px solid #aaa;
    padding: 6px;
    border-radius: 4px;
    color: #000000;
}
QPushButton:hover {
    background-color: #d0d0d0;
}
QTabWidget::pane {
    border: 1px solid #ccc;
}
QTabBar::tab {
    background: #e0e0e0;
    padding: 6px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #d0d0d0;
}
QLabel#section_label {
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 10px;
}
"""

toggle_style = """
QCheckBox {
    spacing: 10px;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 40px;
    height: 20px;
    border-radius: 10px;
    background: #888;  /* cinza desativado */
}

QCheckBox::indicator:checked {
    background: #fff;  /* branco ativado */
}
"""

# ----- Toggle button MainTab -----
toggle_button_style_start = """
QPushButton {
    font-size: 18px;
    font-weight: bold;
    color: white;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #66bb6a, stop:1 #43a047);
    border-radius: 12px;
    border: 2px solid #388e3c;
    padding: 10px 20px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #81c784, stop:1 #4caf50);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #43a047, stop:1 #388e3c);
    padding-left: 12px;
    padding-top: 12px;
}
"""

toggle_button_style_stop = """
QPushButton {
    font-size: 18px;
    font-weight: bold;
    color: white;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ef5350, stop:1 #e53935);
    border-radius: 12px;
    border: 1px solid #c62828;
    padding: 10px 20px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e57373, stop:1 #f44336);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e53935, stop:1 #c62828);
    padding-left: 12px;
    padding-top: 12px;
}
"""

