from PyQt4 import QtGui, QtCore

from sympy.geometry import Segment

import settings
from graphics_items.base_item import BaseItem
from graphics_items.point_graphics_item import PointGraphicsItem, MidPoint


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
        self.point1_item = PointGraphicsItem(self.point1)
        self.add_child(self.point1_item)

        # End Point
        self.point2_item = PointGraphicsItem(self.point2)
        self.add_child(self.point2_item)

        # Mid Point
        # TODO: Set deleteable = false
        # TODO: Set only visible on PointInput
        self.midpoint_item = MidPoint(self.segment.midpoint)
        self.add_child(self.midpoint_item)


class SegmentGraphicsItem(QtGui.QGraphicsLineItem):
    def __init__(self, point1, point2):

        self.hover = False

        self.point1 = point1
        self.point2 = point2

        super(SegmentGraphicsItem, self).__init__(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y)

        self.pen_thickness = 1
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

    def hoverEnterEvent(self, event):
        super(SegmentGraphicsItem, self).hoverEnterEvent(event)
        self.hover = True
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.pen_thickness))

    def hoverLeaveEvent(self, event):
        super(SegmentGraphicsItem, self).hoverLeaveEvent(event)
        self.hover = False
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness))

    def shape(self):
        p = QtGui.QPainterPath(QtCore.QPointF(self.point1.x, self.point1.y))
        p.lineTo(self.point2.x, self.point2.y)

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path

    def paint(self, painter, option, widget):
        # Disable dotted selection rectangle
        option = QtGui.QStyleOptionGraphicsItem(option)
        option.state &= ~ QtGui.QStyle.State_Selected

        if self.hover:
            self.setPen(QtGui.QPen(QtCore.Qt.red, self.pen_thickness))
        else:
            self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness))

        if self.isSelected():
            self.setPen(QtGui.QPen(QtCore.Qt.green, self.pen_thickness))

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
            painter.drawPath(self.shape())

        super(SegmentGraphicsItem, self).paint(painter, option, widget)
