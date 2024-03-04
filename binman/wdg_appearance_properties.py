import avbutils
from PySide6 import QtWidgets, QtCore, QtGui

class AppearancePropertiesPanel(QtWidgets.QWidget):
	"""Bin display properties"""

	thumb_size_frame_changed = QtCore.Signal(int)

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
		self.thumb_size_frame_slider.valueChanged.connect(self.thumb_size_frame_changed)
		self.grp_display_modes.layout().addRow("Thumbnail Size (Frame Mode):", self.thumb_size_frame_slider)

		self.thumb_size_script_slider = QtWidgets.QSlider(minimum=avbutils.THUMB_SCRIPT_MODE_RANGE.start, maximum=avbutils.THUMB_SCRIPT_MODE_RANGE.stop, orientation=QtCore.Qt.Orientation.Horizontal)
		self.grp_display_modes.layout().addRow("Thumbnail Size (Script Mode):", self.thumb_size_script_slider)

		self.layout().addWidget(self.grp_display_modes)

		self.grp_font = QtWidgets.QGroupBox(title="Bin Font Settings")
		self.grp_font.setLayout(QtWidgets.QFormLayout())

		self.font_layout = QtWidgets.QHBoxLayout()

		self.font_list = QtWidgets.QComboBox()
		self.font_list.addItems(QtGui.QFontDatabase.families())

		self.font_size = QtWidgets.QSpinBox(minimum=avbutils.FONT_SIZE_RANGE.start, maximum=avbutils.FONT_SIZE_RANGE.stop)

		self.font_layout.addWidget(self.font_list)
		self.font_layout.addWidget(self.font_size)
		self.grp_font.layout().addRow("Bin Font:", self.font_layout)


		self.btn_color_bg = QtWidgets.QPushButton()
		self.btn_color_bg.setProperty("color", QtGui.QColor())
		self.btn_color_bg.clicked.connect(lambda:self.choose_color(self.btn_color_bg))

		self.btn_color_fg = QtWidgets.QPushButton()
		self.btn_color_fg.setProperty("color", QtGui.QColor())
		self.btn_color_fg.clicked.connect(lambda:self.choose_color(self.btn_color_fg))

		self.grp_font.layout().addRow("Foreground Color:", self.btn_color_fg)
		self.grp_font.layout().addRow("Background Color:", self.btn_color_bg)

		self.layout().addWidget(self.grp_font)

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
	
	def choose_color(self, color_button:QtWidgets.QPushButton):

		new_color = QtWidgets.QColorDialog.getColor(initial=color_button.property("color"))
		if new_color.isValid():
			self.set_color(color_button, new_color)
	
	def set_color(self, color_button:QtWidgets.QPushButton, color:QtGui.QColor):
		color_button.setProperty("color", color)
		color_button.setStyleSheet(f"background-color: {color.name()};")
	
	def set_bg_color(self, color:QtGui.QColor):
		self.set_color(self.btn_color_bg, color)

	def set_fg_color(self, color:QtGui.QColor):
		self.set_color(self.btn_color_fg, color)
			
	
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