from PyQt4 import QtGui, QtCore

from sympy.geometry import Point, Segment

import settings
from graphics_items.base_item import BaseItem
from graphics_items.base_graphics_item import BaseGraphicsItem
from graphics_items.point_graphics_item import CenterPoint, QuarterPoint
from graphics_items.segment_graphics_item import HorizontalSnap, VerticalSnap


class CircleItem(BaseItem):
    def __init__(self, point1, point2, *args, **kwargs):
        super(CircleItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        circle_item = CircleGraphicsItem(self.point1, self.point2)
        self.add_child(circle_item)

        # Snap Points
        center_point_item = CenterPoint(self.point1)
        self.add_child(center_point_item)

        quarter_points = [
            Point(self.point1.x, self.point1.y + circle_item.radius),
            Point(self.point1.x, self.point1.y - circle_item.radius),
            Point(self.point1.x + circle_item.radius, self.point1.y),
            Point(self.point1.x - circle_item.radius, self.point1.y)
        ]

        for point in quarter_points:
            self.add_child(QuarterPoint(point))

        h_segment = HorizontalSnap(
            Point(self.point1.x - circle_item.radius * 20.0, self.point1.y - circle_item.radius),
            Point(self.point1.x + circle_item.radius * 20.0, self.point1.y - circle_item.radius)
        )
        self.add_child(h_segment)


        v_segment = VerticalSnap(
            Point(self.point1.x + circle_item.radius, self.point1.y - circle_item.radius * 20.0),
            Point(self.point1.x + circle_item.radius, self.point1.y + circle_item.radius * 20.0)
        )
        self.add_child(v_segment)


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
