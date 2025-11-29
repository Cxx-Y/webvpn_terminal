import sys
from PySide6.QtWidgets import QApplication
from ui.window import MainWindow

def load_qss(app):
    try:
        with open("resources/style.qss", "r", encoding="utf8") as f:
            app.setStyleSheet(f.read())
    except:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_qss(app)

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
