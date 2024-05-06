#!/usr/bin/env python
from PySide6 import QtWidgets

from .wdg_appearance_properties import AppearancePropertiesPanel
from .wdg_frameview import FrameView
from .wdg_menus import BinmanMenuBar
from .wdg_bin_listview import BinItemsTree, BinHeadersTreeView
from .wdg_binview_properties import BinViewPanel
from .wnd_main import BinmanMainWindow, BinmanMain
from .wnd_about import BinmanAbout

APP_NAME:str = "Binman"

class BinmanApp(QtWidgets.QApplication):
	"""Binman"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setApplicationDisplayName(APP_NAME)