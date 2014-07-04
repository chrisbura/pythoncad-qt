
from PyQt4 import QtGui

from graphics_items.base_preview_graphics_item import BasePreviewGraphicsItem
from graphics_items.point_graphics_item import PointGraphicsItem


class RectanglePreviewGraphicsItem(BasePreviewGraphicsItem):
    def __init__(self, point, *args, **kwargs):
        super(RectanglePreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.point = point

        self.line1 = QtGui.QGraphicsLineItem()
        self.line2 = QtGui.QGraphicsLineItem()
        self.line3 = QtGui.QGraphicsLineItem()
        self.line4 = QtGui.QGraphicsLineItem()

        self.add_preview_item(self.line1)
        self.add_preview_item(self.line2)
        self.add_preview_item(self.line3)
        self.add_preview_item(self.line4)

        self.point1 = PointGraphicsItem(self.point)
        self.add_preview_item(self.point1)

    def update(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()

        self.line1.setLine(self.point.x, self.point.y, x, self.point.y)
        self.line2.setLine(x, self.point.y, x, y)
        self.line3.setLine(x, y, self.point.x, y)
        self.line4.setLine(self.point.x, y, self.point.x, self.point.y)
