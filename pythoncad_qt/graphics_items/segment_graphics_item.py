from PyQt4 import QtGui, QtCore

import settings
from graphics_items.point_graphics_item import PointGraphicsItem


class SegmentGraphicsItem(QtGui.QGraphicsLineItem):
    def __init__(self, point1, point2):
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

    def hoverEnterEvent(self, event):
        super(SegmentGraphicsItem, self).hoverEnterEvent(event)
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.pen_thickness))

    def hoverLeaveEvent(self, event):
        super(SegmentGraphicsItem, self).hoverLeaveEvent(event)
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness))

    def shape(self):
        p = QtGui.QPainterPath(QtCore.QPointF(self.point1.x, self.point1.y))
        p.lineTo(self.point2.x, self.point2.y)

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path

    def paint(self, painter, option, widget):
        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
            painter.drawPath(self.shape())
        super(SegmentGraphicsItem, self).paint(painter, option, widget)


class SegmentGraphicsGroup(QtGui.QGraphicsItemGroup):
    def __init__(self, point1, point2):
        super(SegmentGraphicsGroup, self).__init__()

        self.setHandlesChildEvents(False)

        self.point1 = PointGraphicsItem(point1)
        self.point2 = PointGraphicsItem(point2)
        self.segment = SegmentGraphicsItem(point1, point2)

        self.addToGroup(self.segment)
        self.addToGroup(self.point1)
        self.addToGroup(self.point2)
