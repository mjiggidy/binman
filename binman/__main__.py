import sys
from . import BinmanApp, BinmanMainWindow

app = BinmanApp(sys.argv)

wnd_main = BinmanMainWindow()
wnd_main.show()

app.exec()