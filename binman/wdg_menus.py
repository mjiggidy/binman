import sys
from PySide6 import QtWidgets, QtCore

class BinmanMenuBar(QtWidgets.QMenuBar):

	sig_bin_chosen = QtCore.Signal(QtCore.QFileInfo)
	sig_make_new_bin = QtCore.Signal()

	def __init__(self):
		super().__init__()

		self.mnu_file  = QtWidgets.QMenu("&File")
		self.addMenu(self.mnu_file)
		self.mnu_tools = QtWidgets.QMenu("&Tools")
		self.addMenu(self.mnu_tools)
		self.mnu_help = QtWidgets.QMenu("&Help")
		self.addMenu(self.mnu_help)
		
		self.mnu_file.addAction("&New Bin")
		self.sig_make_new_bin.emit()
		self.act_open = self.mnu_file.addAction("&Open Bin...")
		self.act_open.triggered.connect(self.choose_new_bin)
		self.mnu_file.addSeparator()
		self.act_save = self.mnu_file.addAction("&Save Bin As...")
		self.act_save.triggered.connect(self.choose_save_bin)
		self.mnu_file.addSeparator()
		self.mnu_file.addAction("&Quit")
	
	def choose_new_bin(self):

		bin_path, file_mask = QtWidgets.QFileDialog.getOpenFileName(self, "Choose an Avid bin...", filter="*.avb")
		if not bin_path:
			return

		bin_path = QtCore.QFileInfo(bin_path)
		if not bin_path.isFile():
			print("No", file=sys.stderr)
			return
		
		self.sig_bin_chosen.emit(bin_path)
	
	def choose_save_bin(self):
		bin_path, file_mask = QtWidgets.QFileDialog.getSaveFileName(self, "Save a copy of this bin as...", filter="*.avb")