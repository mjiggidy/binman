from PySide6 import QtWidgets, QtCore

class BinmanMainWindow(QtWidgets.QMainWindow):
	"""Main program window"""
	pass

class BinmanMainWindowController(QtCore.QObject):
	"""Controller for `BinmanMainWindow`"""
	
	def __init__(self, window:BinmanMainWindow, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self._window = window
	
	@property
	def window(self):
		"""Return the `BinmanMainWindow` this is controlling"""
		return self._window