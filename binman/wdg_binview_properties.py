import avb, avbutils
from PySide6 import QtWidgets, QtCore
from . import BinHeadersTreeView


class BinViewPanel(QtWidgets.QWidget):

	sig_show_user_placed_changed = QtCore.Signal(bool)
	sig_show_reference_clips_changed = QtCore.Signal(bool)

	"""Bin display options have been changed"""

	def __init__(self):
		super().__init__()

		self._show_user_placed = False
		self._show_reference_clips = False

		self.setLayout(QtWidgets.QVBoxLayout())


		# Probably should be its own widget?
		self.grp_preset = QtWidgets.QGroupBox("Preset")
		self.grp_preset.setLayout(QtWidgets.QVBoxLayout())

		self.cmb_preset = QtWidgets.QComboBox()
		self.cmb_preset.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Maximum))
		self.cmb_preset.addItem("Default")

		self.btn_save_preset = QtWidgets.QPushButton("+")
		
		lay_controls = QtWidgets.QHBoxLayout()
		lay_controls.addWidget(self.cmb_preset)
		lay_controls.addWidget(self.btn_save_preset)

		#self.grp_preset.layout().addWidget(self.cmb_preset)
		#self.grp_preset.layout().addWidget(self.btn_save_preset)
		
		self.grp_preset.layout().addLayout(lay_controls)
		self.layout().addWidget(self.grp_preset)

		self.tree_columns = BinHeadersTreeView()
		
		self.grp_preset.layout().addWidget(self.tree_columns)
		#self.layout().addWidget(self.tree_columns)


		# Probably should be its own widget?
		self.grp_bin_display = QtWidgets.QGroupBox("Display Items")
		self.grp_bin_display.setLayout(QtWidgets.QVBoxLayout())

		self.chk_user_placed     = QtWidgets.QCheckBox("Show User-Placed Items")
		self.chk_user_placed.stateChanged.connect(self.set_show_user_placed)
		self.chk_reference_clips = QtWidgets.QCheckBox("Show Reference Clips")
		self.chk_reference_clips.stateChanged.connect(self.set_show_reference_clips)

		self.grp_bin_display.layout().addWidget(self.chk_user_placed)
		self.grp_bin_display.layout().addWidget(self.chk_reference_clips)

		self.layout().addWidget(self.grp_bin_display)


	def set_bin_columns_list(self, columns:list):
		self.tree_columns.clear()
		self.tree_columns.addTopLevelItems([BinViewItem(x) for x in columns])
		[self.tree_columns.resizeColumnToContents(x) for x in range(self.tree_columns.columnCount())]
	
	def set_bin_view_name(self, name:str):
		self.cmb_preset.clear()
		self.cmb_preset.addItem(name)
	
	def set_show_user_placed(self, show:bool):

		print("Hi")
		if show == self._show_user_placed:
			return
		
		self._show_user_placed = bool(show)
		self.chk_user_placed.setChecked(self.show_user_placed())
		self.sig_show_user_placed_changed.emit(self.show_user_placed())

	def show_user_placed(self) -> bool:
		return self._show_user_placed
	
	def show_reference_clips(self) -> bool:
		return self._show_reference_clips

	def set_show_reference_clips(self, show:bool):

		if show == self._show_reference_clips:
			return
		
		self._show_reference_clips = bool(show)
		self.chk_reference_clips.setChecked(self.show_reference_clips())
		self.sig_show_reference_clips_changed.emit(self.show_reference_clips())





class BinViewItem(QtWidgets.QTreeWidgetItem):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def __lt__(self, other:QtWidgets.QTreeWidgetItem):
		sort_column = self.treeWidget().sortColumn()
		return avbutils.human_sort(self.text(sort_column)) < avbutils.human_sort(other.text(sort_column))
	
	@classmethod
	def get_column_data(cls, mob:avb.misc.MobRef, headers=None):

		headers = headers or []

		try:
			mastermob = avbutils.matchback_to_masterclip(mob)
			sourcemob = avbutils.matchback_to_sourcemob(mastermob)
		except Exception as e:
			return [mob.name, str(mob), f"Skipping {mob}: {e}"]
		
		#print(mastermob.attributes)
		
		data = []
		for header in headers:
			if header in mob.attributes:
				data.append(mob.attributes.get(header))
			elif "_USER" in mob.attributes.get("_USER"):
				data.append(mob.attributes.get("_USER").get(header))
			elif header in mastermob.attributes:
				data.append(mastermob.attributes.get(header))
			elif "_USER" in mastermob.attributes:
				data.append(mastermob.attributes.get("_USER").get(header, "???"))
			else:
				data.append("No attributes atom")

		return data