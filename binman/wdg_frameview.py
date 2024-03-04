import math, typing
import avb, avbutils
from PySide6 import QtWidgets, QtCore, QtGui

class FrameViewGraph(QtWidgets.QGraphicsView):

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.grid_scale = avbutils.THUMB_FRAME_MODE_RANGE.stop
	
	def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF | QtCore.QRect) -> None:

		x_unit_size = avbutils.THUMB_UNIT_SIZE[0] * self.grid_scale
		y_unit_size = avbutils.THUMB_UNIT_SIZE[1] * self.grid_scale

		x_segments = 3
		y_segments = 3

		pen_solid = QtGui.QPen(QtCore.Qt.PenStyle.SolidLine)
		pen_dashed = QtGui.QPen(QtCore.Qt.PenStyle.DashLine)

		# math.floor(rect.left() / x_unit_size) * x_unit_size

		x_range = range(int(math.floor(rect.left() / x_unit_size) * x_unit_size), int(rect.right()), int(x_unit_size/x_segments))
		y_range = range(int(math.floor(rect.top() / y_unit_size) * y_unit_size), int(rect.bottom()), int(y_unit_size/y_segments))
		
		for seg_idx, col in enumerate(x_range):
			if seg_idx % x_segments == 0:
				painter.setPen(pen_solid)
			else:
				painter.setPen(pen_dashed)
			painter.drawLine(QtCore.QLine(col, y_range.start, col, y_range.stop))

		for seg_idx, row in enumerate(y_range):
			if seg_idx % y_segments == 0:
				painter.setPen(pen_solid)
			else:
				painter.setPen(pen_dashed)
			painter.drawLine(QtCore.QLine(x_range.start, row, x_range.stop, row))

		

		
		#return super().drawBackground(painter, rect)

class FrameView(QtWidgets.QWidget):

	def __init__(self, scale:typing.Optional[int]=avbutils.THUMB_FRAME_MODE_RANGE.start):

		super().__init__()

		self.scene = QtWidgets.QGraphicsScene()
		self.scale = 1

		self.setLayout(QtWidgets.QVBoxLayout())

		self.frameview = FrameViewGraph(self.scene)
		self.layout().addWidget(self.frameview)

		self.brush_bg = QtGui.QBrush()
		self.brush_bg.setStyle(QtCore.Qt.BrushStyle.CrossPattern)
		self.frameview.setBackgroundBrush(self.brush_bg )
	
	def set_items(self, items:list[avb.bin.BinItem]):
		"""Set the items in the frame view"""

		self.scene.clear()

		for item in (x for x in items if x.user_placed):
			icon = self.scene.addRect(item.x, item.y, avbutils.THUMB_UNIT_SIZE[0] * self.scale, avbutils.THUMB_UNIT_SIZE[1] * self.scale)
			#print("Add", item.x, item.y)
			icon.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		
		self.set_view_scale(self.scale)
		self.frameview.show()

	def set_view_scale(self, scale:int):

		for item in self.scene.items():
			if isinstance(item, QtWidgets.QGraphicsRectItem):
				item.prepareGeometryChange()
				new_rect = QtCore.QRectF(item.rect())
				new_rect.setWidth(avbutils.THUMB_UNIT_SIZE[0] * scale)
				new_rect.setHeight(avbutils.THUMB_UNIT_SIZE[1] * scale)
				item.setRect(new_rect)
				#print(item.rect())
		
		self.frameview.grid_scale = scale
		self.scale = scale
		self.scene.update()
		#for item in self.scene.items():
		#	item.setRect(item.scenePos().x(), item.scenePos().y(), avbutils.THUMB_UNIT_SIZE[0] * scale, avbutils.THUMB_UNIT_SIZE[1] * scale)