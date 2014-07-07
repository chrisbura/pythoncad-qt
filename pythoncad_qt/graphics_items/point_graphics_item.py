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

        self.shape_cache = None

        super(PointGraphicsItem, self).__init__(
            self.entity.x - self.radius,
            self.entity.y - self.radius,
            self.radius * 2.0,
            self.radius * 2.0)

    def shape(self):
        # TODO: Find how to properly handle overzealous shape calculations
        if not self.shape_cache:
            path = QtGui.QPainterPath()
            width = 20.0
            path.addEllipse(self.entity.x - width / 2.0, self.entity.y - width / 2.0, width, width)
            self.shape_cache = path
        return self.shape_cache


class SnapPoint(PointGraphicsItem):
    default_colour = QtCore.Qt.transparent


class MidPoint(SnapPoint):
    pass


class EndPoint(SnapPoint):
    pass


class CenterPoint(SnapPoint):
    pass


class QuarterPoint(SnapPoint):
    pass
