from PySide6 import QtWidgets, QtCore, QtGui
import avb, avbutils

from . import AppearancePropertiesPanel, BinViewPanel, FrameView, BinItemsTree, BinmanMenuBar
from . import binmodel

class BinmanMainWindow(QtWidgets.QMainWindow):

	sig_close_app = QtCore.Signal()
	sig_close_window = QtCore.Signal()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setCentralWidget(BinmanMain())
		
		self.setMenuBar(BinmanMenuBar())
		self.menuBar().sig_make_new_bin.connect(self.centralWidget().load_new_bin)
		self.menuBar().sig_bin_chosen.connect(self.centralWidget().load_bin)
		self.menuBar().sig_quit.connect(self.sig_close_app)
		self.menuBar().sig_close_window.connect(self.close_window)

		self.setStatusBar(QtWidgets.QStatusBar())

		self.resize(1600, 800)


		#self.setTabPosition(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, QtWidgets.QTabWidget.TabPosition.North)
		#self.add_tool(AppearancePropertiesPanel(), "Appearance Properties")
		#self.add_tool(BinViewPanel(), "Bin View")
	
	def add_tool(self, widget:QtWidgets.QWidget, title:str|None=None):

		dock_widget = QtWidgets.QDockWidget()
		dock_widget.setWidget(widget)

		if title:
			dock_widget.setWindowTitle(title)

		self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)
	
	@QtCore.Slot()
	def close_window(self):
		self.close()

	def resizeEvent(self, *args):

		super().resizeEvent(*args)
		self.setWindowTitle(str(self.size()))



class BinmanMain(QtWidgets.QWidget):
	"""Main window component"""

	def __init__(self):
		super().__init__()
		
		self.setLayout(QtWidgets.QHBoxLayout())

		self.tabs_binpreview = QtWidgets.QTabWidget()
		self.tabs_binpreview.setTabsClosable(True)
		self.tabs_binpreview.setMovable(True)

		self.bin_model = binmodel.BinModel()

		self.tree_binitems = BinItemsTree()
		self.tree_binitems.setModel(binmodel.BinModelProxy())
		self.tree_binitems.model().setSourceModel(self.bin_model)


		
		self.tabs_binpreview.addTab(self.tree_binitems, "List View")

		self.frameview = FrameView()
		self.tabs_binpreview.addTab(self.frameview, "Frame View")

		self.layout().addWidget(self.tabs_binpreview)

		self.tabs = QtWidgets.QTabWidget()
		self.tabs.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.MinimumExpanding))
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)
		

		self.panel_displayproperties = AppearancePropertiesPanel()

		self.panel_displayproperties.sig_font_chosen.connect(self.tree_binitems.setFont)

		self.panel_displayproperties.sig_colors_chosen.connect(self.tree_binitems.setColors)


		self.panel_binview = BinViewPanel()

		self.panel_binview.sig_show_reference_clips_changed.connect(self.filters_changed)
		self.panel_binview.sig_show_user_placed_changed.connect(self.filters_changed)

		self.tabs.addTab(self.panel_displayproperties, "Appearance")
		self.tabs.addTab(self.panel_binview, "Bin View")

		self.tabs.addTab(QtWidgets.QWidget(), "Sift && Sort")
		self.tabs.addTab(QtWidgets.QWidget(), "Automation")

		self.layout().addWidget(self.tabs)
		
		self.panel_displayproperties.thumb_size_frame_chosen.connect(self.frameview.set_view_scale)
	
	@QtCore.Slot()
	def filters_changed(self):
		self.tree_binitems.model().filters_changed(
			self.panel_binview.show_user_placed(), self.panel_binview.show_reference_clips()
		)
	
	@QtCore.Slot()
	def new_bin_loaded(self, bin:avb.bin.Bin):

			self.panel_displayproperties.set_mode(avbutils.BinDisplayModes.get_mode_from_bin(bin))
			self.panel_displayproperties.set_thumb_frame_size(bin.mac_image_scale)
			self.panel_displayproperties.set_thumb_script_size(bin.ql_image_scale)

			self.panel_displayproperties.set_font_family_index(bin.mac_font)
			self.panel_displayproperties.set_font_size(bin.mac_font_size)
			
			self.panel_displayproperties.btn_color_bg.setColor(QtGui.QColor(QtGui.QRgba64.fromRgba64(*bin.background_color, 1)))
			self.panel_displayproperties.btn_color_fg.setColor(QtGui.QColor(QtGui.QRgba64.fromRgba64(*bin.forground_color, 1)))

			display_options = avbutils.BinDisplayOptions.get_options_from_bin(bin)
			print(display_options)
			self.panel_binview.set_show_user_placed(avbutils.BinDisplayOptions.SHOW_CLIPS_CREATED_BY_USER in display_options)
			self.panel_binview.set_show_reference_clips(avbutils.BinDisplayOptions.SHOW_REFERENCE_CLIPS in display_options)


			y1,x1, y2,x2 = bin.home_rect
			bin_rect = QtCore.QRect(QtCore.QPoint(x1,y1),QtCore.QPoint(x2,y2))

			self.panel_displayproperties.set_screen_position(bin_rect)
			self.panel_displayproperties.set_screen_size(bin_rect)

			self.panel_binview.set_bin_view_name(bin.view_setting.name)
			self.panel_binview.set_bin_columns_list(
				[[str(idx+1), col.get("title"),str(avbutils.BinColumnFormat(col.get("format"))), str(col.get("type")), str(int(col.get("hidden")))] for idx, col in enumerate(bin.view_setting.columns)]
			)



			self.tree_binitems.resizeColumnToContents(0)

			self.frameview.set_items(bin.items)
			self.frameview.set_view_scale(bin.mac_image_scale)
			print("Scaling to", bin.mac_image_scale)
	
	@QtCore.Slot()
	def load_bin(self, bin_path:QtCore.QFileInfo):

		print("Opening ", bin_path.absoluteFilePath())

		try:
			self.bin_handle.close()
		except Exception as e:
			print("While closing:", str(e))

		print("Opening", str(bin_path))

		self.bin_handle =avb.open(bin_path.absoluteFilePath())
		bin = self.bin_handle.content
		self.bin_model.setBin(bin)
		self.parent().setWindowFilePath(bin_path.absoluteFilePath())
		self.new_bin_loaded(bin)
	
	@QtCore.Slot()
	def load_new_bin(self):
		print("Creating new bin...")
		self.bin_handle = avb.file.AVBFile()
		bin = self.bin_handle.content
		self.setWindowFilePath("Untitled Bin")
		self.new_bin_loaded(bin)