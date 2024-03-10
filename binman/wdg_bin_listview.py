from PySide6 import QtWidgets, QtCore, QtGui

class BinItemsTree(QtWidgets.QTreeView):
	"""Bin items"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def setColors(self, fg_color:QtGui.QColor, bg_color:QtGui.QColor):

		self.setStyleSheet(f"color: {fg_color.name(QtGui.QColor.NameFormat.HexRgb)}; background-color: {bg_color.darker(105).name(QtGui.QColor.NameFormat.HexRgb)}; alternate-background-color: {bg_color.lighter(105).name(QtGui.QColor.NameFormat.HexRgb)}")

		print("FG:", fg_color.name(QtGui.QColor.NameFormat.HexRgb))
		print("BG:", bg_color.name(QtGui.QColor.NameFormat.HexRgb))
