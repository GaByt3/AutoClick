from gui import *
from styles import dark_style

app = QApplication(sys.argv)
app.setStyleSheet(dark_style) 

window = AutoClickUI()
window.show()
sys.exit(app.exec_())
