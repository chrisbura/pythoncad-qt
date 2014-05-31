from PyQt4 import QtGui, QtCore

import settings
from graphics_items.base_item import BaseItem
from graphics_items.base_graphics_item import BaseGraphicsItem, FilledShapeMixin


class PointItem(BaseItem):
    def __init__(self, point, *args, **kwargs):
        super(PointItem, self).__init__(*args, **kwargs)

        self.point_item = PointGraphicsItem(point)
        self.add_child(self.point_item)


class PointGraphicsItem(FilledShapeMixin, BaseGraphicsItem, QtGui.QGraphicsEllipseItem):
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
    default_colour = QtCore.Qt.transparent
