from PySide6 import QtWidgets, QtCore, QtGui
import avbutils

class BinItemsTree(QtWidgets.QTreeView):
	"""Bin items"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding))
		self.setAlternatingRowColors(True)
		self.setSortingEnabled(True)
		self.setIndentation(0)
		
		self.setItemDelegate(avbutils.binmodel.BinItemDisplayDelegate())

	def setColors(self, fg_color:QtGui.QColor, bg_color:QtGui.QColor):

		color_bg_base = bg_color.darker(105).name()
		color_bg_alternate = bg_color.lighter(105).name()

		self.setStyleSheet(f"color: {fg_color.name(QtGui.QColor.NameFormat.HexRgb)}; background-color: {color_bg_base}; alternate-background-color: {color_bg_alternate};")

		print("FG:", fg_color.name(QtGui.QColor.NameFormat.HexRgb))
		print("BG:", bg_color.name(QtGui.QColor.NameFormat.HexRgb))

class BinHeadersTreeView(QtWidgets.QTreeWidget):

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.setHeaderLabels(("#", "Name", "Display Format", "Data Type","Hidden"))
		self.setAlternatingRowColors(True)
		self.setIndentation(0)
		self.resizeColumnToContents(0)
		self.setSortingEnabled(True)
		self.setSelectionMode(QtWidgets.QTreeWidget.SelectionMode.ExtendedSelection)
		self.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)