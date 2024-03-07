import sys
from PySide6 import QtWidgets, QtCore, QtGui

class BinmanMenuBar(QtWidgets.QMenuBar):

	sig_bin_chosen = QtCore.Signal(QtCore.QFileInfo)
	sig_make_new_bin = QtCore.Signal()

	sig_close_window = QtCore.Signal()
	sig_quit = QtCore.Signal()

	sig_show_about = QtCore.Signal()

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
		
		self.act_quit = self.mnu_file.addAction("&Quit")
		self.act_quit.triggered.connect(self.sig_quit)


		self.act_about = self.mnu_help.addAction("About Binman...")
		self.act_about.triggered.connect(self.sig_show_about)
		
	
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