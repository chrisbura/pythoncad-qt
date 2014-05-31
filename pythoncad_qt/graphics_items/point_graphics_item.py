from PyQt4 import QtGui, QtCore

import settings
from graphics_items.base_item import BaseItem
from graphics_items.base_graphics_item import BaseGraphicsItem


class PointItem(BaseItem):
    def __init__(self, point, *args, **kwargs):
        super(PointItem, self).__init__(*args, **kwargs)

        self.point_item = PointGraphicsItem(point)
        self.add_child(self.point_item)


class PointGraphicsItem(BaseGraphicsItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, point):
        self.entity = point
        self.radius = 2.0

        super(PointGraphicsItem, self).__init__(
            self.entity.x - self.radius,
            self.entity.y - self.radius,
            self.radius * 2.0,
            self.radius * 2.0)

    def shape(self):
        shape = super(PointGraphicsItem, self).shape()
        path = QtGui.QPainterPath()
        width = 20.0
        path.addEllipse(self.entity.x - width / 2.0, self.entity.y - width / 2.0, width, width)
        return path


class MidPoint(PointGraphicsItem):

    def __init__(self, *args, **kwargs):
        super(MidPoint, self).__init__(*args, **kwargs)
        self.setPen(QtGui.QPen(QtCore.Qt.transparent, settings.ITEM_PEN_THICKNESS, QtCore.Qt.SolidLine))
        self.setBrush(QtCore.Qt.transparent)

    def hoverEnterEvent(self, event):
        super(MidPoint, self).hoverEnterEvent(event)
        self.setBrush(QtCore.Qt.black)
        self.setPen(QtGui.QPen(QtCore.Qt.black, settings.ITEM_PEN_THICKNESS))

    def hoverLeaveEvent(self, event):
        super(MidPoint, self).hoverLeaveEvent(event)
        self.setBrush(QtCore.Qt.transparent)
        self.setPen(QtGui.QPen(QtCore.Qt.transparent, settings.ITEM_PEN_THICKNESS))
