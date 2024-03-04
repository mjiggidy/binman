import sys
from PySide6 import QtCore
from . import BinmanApp, BinmanMainWindow

app = BinmanApp(sys.argv)

wnd_main = BinmanMainWindow()
wnd_main.show()

if len(sys.argv) > 1:
	wnd_main.centralWidget().load_bin(QtCore.QFileInfo(sys.argv[1]))
else:
	wnd_main.centralWidget().load_new_bin()

app.exec()