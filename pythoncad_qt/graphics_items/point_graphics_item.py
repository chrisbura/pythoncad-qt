from PyQt4 import QtGui, QtCore

import settings


class PointGraphicsItem(QtGui.QGraphicsEllipseItem):
    def __init__(self, point):
        self.entity = point
        self.radius = 2.0

        super(PointGraphicsItem, self).__init__(
            self.entity.x - self.radius,
            self.entity.y - self.radius,
            self.radius * 2.0,
            self.radius * 2.0)

        self.pen_thickness = 1
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness, QtCore.Qt.SolidLine))
        self.setBrush(QtCore.Qt.black)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        super(PointGraphicsItem, self).hoverEnterEvent(event)
        self.setBrush(QtCore.Qt.red)
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.pen_thickness))

    def hoverLeaveEvent(self, event):
        super(PointGraphicsItem, self).hoverLeaveEvent(event)
        self.setBrush(QtCore.Qt.black)
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness))

    def shape(self):
        shape = super(PointGraphicsItem, self).shape()
        path = QtGui.QPainterPath()
        width = 10.0
        path.addEllipse(self.entity.x - width / 2.0, self.entity.y - width / 2.0, width, width)
        return path

    def paint(self, painter, option, widget):
        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
            painter.drawPath(self.shape())
        super(PointGraphicsItem, self).paint(painter, option, widget)
