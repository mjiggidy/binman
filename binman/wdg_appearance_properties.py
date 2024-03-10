import avbutils
from PySide6 import QtWidgets, QtCore, QtGui

class ColorPickerButton(QtWidgets.QPushButton):
	"""A little button you can click and it chooses a color. Isn't that nice?"""

	sig_color_changed = QtCore.Signal(QtGui.QColor)
	"""A color has been chosen"""

	def __init__(self, color:QtGui.QColor|None=None, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.clicked.connect(self.choose_color)
		self.setColor(color or QtGui.QColor())
	
	@QtCore.Slot()
	def choose_color(self):
		new_color = QtWidgets.QColorDialog.getColor(initial=self.property("color"))
		if new_color.isValid():
			self.setColor(new_color)
	
	@QtCore.Slot(QtGui.QColor)
	def setColor(self, color:QtGui.QColor):
		"""Set the color of this picker"""
		self.setProperty("color", color)
		self.setStyleSheet(f"background-color: {self.color().name(QtGui.QColor.NameFormat.HexRgb)}")
		self.sig_color_changed.emit(self.color())
	
	def color(self) -> QtGui.QColor:
		"""The current color that has been chosen"""
		return self.property("color")



class AppearancePropertiesPanel(QtWidgets.QWidget):
	"""Bin display properties"""

	thumb_size_frame_chosen = QtCore.Signal(int)
	sig_font_chosen = QtCore.Signal(QtGui.QFont)
	sig_colors_chosen = QtCore.Signal(QtGui.QColor, QtGui.QColor)

	def __init__(self):
		super().__init__()
		self.setLayout(QtWidgets.QVBoxLayout())

		self.grp_display_modes = QtWidgets.QGroupBox(title="Bin Presentation")
		self.grp_display_modes.setLayout(QtWidgets.QFormLayout())

		display_modes = [(mode.value, mode.name.replace("_"," ").title()) for mode in avbutils.BinDisplayModes]

		self.display_modes_group = QtWidgets.QButtonGroup()
		self.display_modes_layout = QtWidgets.QHBoxLayout()
		for mode in display_modes:
			btn_mode = QtWidgets.QRadioButton(mode[1])
			btn_mode.setProperty("mode_index", mode[0])
			self.display_modes_group.addButton(btn_mode)
			self.display_modes_layout.addWidget(btn_mode)
		
		self.grp_display_modes.layout().addRow("Display Mode:", self.display_modes_layout)


		self.thumb_size_frame_slider = QtWidgets.QSlider(minimum=avbutils.THUMB_FRAME_MODE_RANGE.start, maximum=avbutils.THUMB_FRAME_MODE_RANGE.stop, orientation=QtCore.Qt.Orientation.Horizontal)
		self.thumb_size_frame_slider.valueChanged.connect(self.thumb_size_frame_chosen)
		self.grp_display_modes.layout().addRow("Thumbnail Size (Frame Mode):", self.thumb_size_frame_slider)

		self.thumb_size_script_slider = QtWidgets.QSlider(minimum=avbutils.THUMB_SCRIPT_MODE_RANGE.start, maximum=avbutils.THUMB_SCRIPT_MODE_RANGE.stop, orientation=QtCore.Qt.Orientation.Horizontal)
		self.grp_display_modes.layout().addRow("Thumbnail Size (Script Mode):", self.thumb_size_script_slider)

		self.layout().addWidget(self.grp_display_modes)

		self.grp_font = QtWidgets.QGroupBox(title="Bin Font Settings")
		self.grp_font.setLayout(QtWidgets.QFormLayout())

		self.font_layout = QtWidgets.QHBoxLayout()

		self.font_list = QtWidgets.QComboBox()
		self.font_list.addItems(QtGui.QFontDatabase.families())
		self.font_list.currentIndexChanged.connect(lambda:self.sig_font_chosen.emit(self.user_font()))

		self.font_size = QtWidgets.QSpinBox(minimum=avbutils.FONT_SIZE_RANGE.start, maximum=avbutils.FONT_SIZE_RANGE.stop)
		self.font_size.valueChanged.connect(lambda:self.sig_font_chosen.emit(self.user_font()))

		self.font_layout.addWidget(self.font_list)
		self.font_layout.addWidget(self.font_size)
		self.grp_font.layout().addRow("Bin Font:", self.font_layout)
		self.layout().addWidget(self.grp_font)


		self.btn_color_bg = ColorPickerButton()
		self.btn_color_fg = ColorPickerButton()

		self.btn_color_fg.sig_color_changed.connect(lambda:self.sig_colors_chosen.emit(*self.bin_colors()))
		self.btn_color_bg.sig_color_changed.connect(lambda:self.sig_colors_chosen.emit(*self.bin_colors()))

		self.grp_font.layout().addRow("Foreground Color:", self.btn_color_fg)
		self.grp_font.layout().addRow("Background Color:", self.btn_color_bg)


		self.grp_position = QtWidgets.QGroupBox(title="Bin Position && Sizing")
		self.grp_position.setLayout(QtWidgets.QFormLayout())

		self.coord_layout = QtWidgets.QHBoxLayout()
		self.coord_x      = QtWidgets.QSpinBox()
		self.coord_x.setRange(-100000, 100000)
		self.coord_y      = QtWidgets.QSpinBox()
		self.coord_y.setRange(-100000, 100000)

		self.coord_layout.addWidget(QtWidgets.QLabel("X:", alignment=QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignCenter))
		self.coord_layout.addWidget(self.coord_x)

		self.coord_layout.addWidget(QtWidgets.QLabel("Y:", alignment=QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignCenter))
		self.coord_layout.addWidget(self.coord_y)

		self.grp_position.layout().addRow("Position On Screen:", self.coord_layout)

		self.sizing_layout = QtWidgets.QHBoxLayout()
		self.sizing_x      = QtWidgets.QSpinBox()
		self.sizing_x.setRange(-100000, 100000)
		self.sizing_y      = QtWidgets.QSpinBox()
		self.sizing_y.setRange(-100000, 100000)

		self.sizing_layout.addWidget(QtWidgets.QLabel("W:", alignment=QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignCenter))
		self.sizing_layout.addWidget(self.sizing_x)

		self.sizing_layout.addWidget(QtWidgets.QLabel("H:", alignment=QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignCenter))
		self.sizing_layout.addWidget(self.sizing_y)

		self.grp_position.layout().addRow("Size On Screen:", self.sizing_layout)

		self.layout().addWidget(self.grp_position)

		self.layout().addStretch()
		
		
		#for idx, font in enumerate(QtGui.QFontDatabase.families()):
		#	print(idx, font)
	
	def user_font(self) -> QtGui.QFont:
		return QtGui.QFont(
			self.font_list.currentText(),
			self.font_size.value()
		)
	
	def bin_colors(self) -> tuple[QtGui.QColor, QtGui.QColor]:
		return self.btn_color_fg.color(), self.btn_color_bg.color()
	
	def set_mode(self, mode:avbutils.BinDisplayModes):
		"""Set the current mode"""

		for button in self.display_modes_group.buttons():
			if button.property("mode_index") == mode.value:
				button.setChecked(True)
				break
	
	def set_thumb_frame_size(self, size:int):
		"""Set the thumbnail size for Frame Mode"""

		self.thumb_size_frame_slider.setValue(size)

	def set_thumb_script_size(self, size:int):
		"""Set the thumbnail size for Frame Mode"""

		self.thumb_size_script_slider.setValue(size)
	
	def set_font_family_index(self, index:int):
		#print(index, " + ", FONT_INDEX_OFFSET)
		self.font_list.setCurrentIndex(index - avbutils.FONT_INDEX_OFFSET)

	def set_font_size(self, size:int):
		self.font_size.setValue(size)
	

	def set_screen_position(self, rectangle=QtCore.QRect):		
		self.coord_x.setValue(rectangle.x())
		self.coord_y.setValue(rectangle.y())
	
	def set_screen_size(self, rectangle=QtCore.QRect):
		self.sizing_x.setValue(rectangle.width())
		self.sizing_y.setValue(rectangle.height())