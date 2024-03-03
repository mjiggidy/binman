from . import BinmanApp, BinmanMainWindow
from PySide6 import QtWidgets

app = BinmanApp()

wnd_main = BinmanMainWindow()
wnd_main.show()

app.exec()