from PySide6 import QtWidgets, QtGui

class BinmanAbout(QtWidgets.QDialog):

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.setWindowTitle("About Binman")

		self.setLayout(QtWidgets.QHBoxLayout())

		self.logo = QtWidgets.QLabel()
		self.logo.setPixmap(QtGui.QPixmap("binman/32x32.png"))
		self.layout().addWidget(self.logo)

		self.lay_about_text = QtWidgets.QVBoxLayout()
		self.lay_about_text.addWidget(QtWidgets.QLabel("<strong style=\"font-size:16px;\">binman</strong>"))
		self.lay_about_text.addWidget(QtWidgets.QLabel("Little utilities for Avid bin management."))
		self.lay_about_text.addWidget(QtWidgets.QLabel("By Michael Jordan &lt;<a href=\"mailto:michael@glowingpixel.com?subject=i%20like%20binman\">michael@glowingpixel.com</a>&gt;"))
		
		self.layout().addLayout(self.lay_about_text)