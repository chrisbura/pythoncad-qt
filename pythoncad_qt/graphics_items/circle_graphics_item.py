from PyQt4 import QtGui, QtCore

from sympy.geometry import Segment

import settings
from graphics_items.base_item import BaseItem
from graphics_items.base_graphics_item import BaseGraphicsItem
from graphics_items.point_graphics_item import PointGraphicsItem


class CircleItem(BaseItem):
    def __init__(self, point1, point2, *args, **kwargs):
        super(CircleItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        center_point_item = PointGraphicsItem(self.point1)
        self.add_child(center_point_item)

        circle_item = CircleGraphicsItem(self.point1, self.point2)
        self.add_child(circle_item)


class CircleGraphicsItem(BaseGraphicsItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, point1, point2):

        self.shape_cache = None

        self.point1 = point1
        self.point2 = point2

        radius_segment = Segment(self.point1, self.point2)
        self.radius = radius_segment.length
        diameter = self.radius * 2.0

        super(CircleGraphicsItem, self).__init__(
            self.point1.x - self.radius,
            self.point1.y - self.radius,
            diameter,
            diameter
        )

    def shape(self):
        # Cache the shape call so that we don't recaulate the stroke unless it
        # changes
        # TODO: Invalidate cache when geometry changes
        if not self.shape_cache:
            shape = super(CircleGraphicsItem, self).shape()
            stroker = QtGui.QPainterPathStroker()
            stroker.setWidth(10.0)
            # simplified removes the 2 extra paths from the three (inside radius,
            # center, and outside radius)
            self.shape_cache = stroker.createStroke(shape).simplified()
        return self.shape_cache
