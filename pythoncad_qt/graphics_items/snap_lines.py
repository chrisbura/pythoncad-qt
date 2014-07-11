
from PyQt4 import QtCore, QtGui

from sympy.geometry import Point

import settings

class SnapSegment(QtGui.QGraphicsLineItem):

    def __init__(self, point1, point2):

        self.point1, self.point2 = point1, point2

        super(SnapSegment, self).__init__(
            point1.x, point1.y,
            point2.x, point2.y
        )
        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

        self.setZValue(-10)

        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtCore.Qt.transparent)
        self.setPen(pen)

    def shape(self):
        p = QtGui.QPainterPath(QtCore.QPointF(self.point1.x, self.point1.y))
        p.lineTo(self.point2.x, self.point2.y)

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(20.0)
        path = stroker.createStroke(p)

        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
        painter.drawPath(self.shape())
        super(SnapSegment, self).paint(painter, option, widget)


class HorizontalSnap(SnapSegment):

    def __init__(self, point):
        self.point = point
        super(HorizontalSnap, self).__init__(
            Point(point.x - 100, point.y),
            Point(point.x + 100, point.y)
        )

    def hoverEnterEvent(self, event):
        super(HorizontalSnap, self).hoverEnterEvent(event)
        self.parent.lock_horizontal.emit(self.point.y)

    def hoverLeaveEvent(self, event):
        super(HorizontalSnap, self).hoverLeaveEvent(event)
        self.parent.hover_leave.emit()


class VerticalSnap(SnapSegment):

    def __init__(self, point):
        self.point = point
        super(VerticalSnap, self).__init__(
            Point(point.x, point.y - 100),
            Point(point.x, point.y + 100)
        )

    def hoverEnterEvent(self, event):
        super(VerticalSnap, self).hoverEnterEvent(event)
        self.parent.lock_vertical.emit(self.point.x)

    def hoverLeaveEvent(self, event):
        super(VerticalSnap, self).hoverLeaveEvent(event)
        self.parent.hover_leave.emit()
