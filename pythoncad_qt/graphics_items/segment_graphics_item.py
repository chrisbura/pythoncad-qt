from PyQt4 import QtGui, QtCore

from sympy.geometry import Segment

import settings
from graphics_items.base_item import BaseItem
from graphics_items.base_graphics_item import BaseGraphicsItem
from graphics_items.point_graphics_item import PointGraphicsItem, MidPoint, EndPoint


class SegmentItem(BaseItem):
    def __init__(self, point1, point2, *args, **kwargs):
        super(SegmentItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        self.segment = Segment(self.point1, self.point2)

        # Segment
        self.segment_item = SegmentGraphicsItem(self.point1, self.point2)
        self.add_child(self.segment_item)

        # Start Point
        self.point1_item = EndPoint(self.point1)
        self.add_child(self.point1_item)

        # End Point
        self.point2_item = EndPoint(self.point2)
        self.add_child(self.point2_item)

        # Mid Point
        # TODO: Set deleteable = false
        # TODO: Set only visible on PointInput
        self.midpoint_item = MidPoint(self.segment.midpoint)
        self.add_child(self.midpoint_item)


class SegmentGraphicsItem(BaseGraphicsItem, QtGui.QGraphicsLineItem):
    def __init__(self, point1, point2):

        self.point1 = point1
        self.point2 = point2

        super(SegmentGraphicsItem, self).__init__(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y)

    def shape(self):
        p = QtGui.QPainterPath(QtCore.QPointF(self.point1.x, self.point1.y))
        p.lineTo(self.point2.x, self.point2.y)

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path


class SnapSegment(SegmentGraphicsItem):
    default_colour = QtCore.Qt.transparent
    hover_colour = QtCore.Qt.transparent

    def __init__(self, *args, **kwargs):
        super(SnapSegment, self).__init__(*args, **kwargs)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)


class HorizontalSnap(SnapSegment):
    pass


class VerticalSnap(SnapSegment):
    pass
