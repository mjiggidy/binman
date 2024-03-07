import sys
from PySide6 import QtCore
from . import BinmanApp, BinmanMainWindow, BinmanAbout

sys.argv += ['-platform', 'windows:darkmode=1']

app = BinmanApp(sys.argv)
app.setStyle("fusion")

wnd_main = BinmanMainWindow()
wnd_main.sig_close_app.connect(app.quit)
wnd_main.menuBar().sig_show_about.connect(lambda:BinmanAbout(wnd_main).exec())
wnd_main.show()

if len(sys.argv) > 1:
	wnd_main.centralWidget().load_bin(QtCore.QFileInfo(sys.argv[1]))
else:
	wnd_main.centralWidget().load_new_bin()

app.exec()