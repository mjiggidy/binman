from PySide6 import QtWidgets, QtCore, QtGui

class BinItemsTree(QtWidgets.QTreeView):
	"""Bin items"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)