

from PyQt4 import QtCore, QtGui

import settings

class SnapLineManager(QtCore.QObject):

    new_line = QtCore.pyqtSignal(object)
    lock_horizontal = QtCore.pyqtSignal(float)
    unlock_horizontal = QtCore.pyqtSignal()
    lock_vertical = QtCore.pyqtSignal(float)
    unlock_vertical = QtCore.pyqtSignal()

    def __init__(self, rect, *args, **kwargs):
        super(SnapLineManager, self).__init__(*args, **kwargs)
        self.horizontal = {}
        self.vertical = {}
        self.rect = rect

    def add_snaplines(self, items):
        for item in items:
            for y in item.horizontal_snap_points():
                line = self.get_horizontal(y)
                line.add_point(item)

            for x in item.vertical_snap_points():
                line = self.get_vertical(x)
                line.add_point(item)

    def get_horizontal(self, y):
        try:
            line = self.horizontal[y]
        except KeyError:
            line = HorizontalSnapLine(self.rect, y)
            self.horizontal[y] = line
            self.new_line.emit(line.scene_item())
            line.lock_horizontal.connect(self.lock_horizontal.emit)
            line.unlock_horizontal.connect(self.unlock_horizontal.emit)
        return line

    def get_vertical(self, x):
        try:
            line = self.vertical[x]
        except KeyError:
            line = VerticalSnapLine(self.rect, x)
            self.vertical[x] = line
            self.new_line.emit(line.scene_item())
            line.lock_vertical.connect(self.lock_vertical.emit)
            line.unlock_vertical.connect(self.unlock_vertical.emit)
        return line


class SnapLineSceneItem(QtGui.QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super(SnapLineSceneItem, self).__init__(*args, **kwargs)

        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.transparent)

        pen.setWidth(1)
        self.setPen(pen)
        self.setZValue(-100)

        self.setAcceptHoverEvents(True)

    def shape(self):
        p = QtGui.QPainterPath(self.line().p1())
        p.lineTo(self.line().p2())

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(15.0)
        path = stroker.createStroke(p)

        return path

    def paint(self, painter, option, widget):
        if settings.DEBUG_SNAP_LINES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())
        super(SnapLineSceneItem, self).paint(painter, option, widget)


class HorizontalSnapLineSceneItem(SnapLineSceneItem):

    def hoverEnterEvent(self, event):
        super(HorizontalSnapLineSceneItem, self).hoverEnterEvent(event)
        self.parent.lock_horizontal.emit(self.line().y1())

    def hoverLeaveEvent(self, event):
        super(HorizontalSnapLineSceneItem, self).hoverLeaveEvent(event)
        self.parent.unlock_horizontal.emit()


class VerticalSnapLineSceneItem(SnapLineSceneItem):
    def hoverEnterEvent(self, event):
        super(VerticalSnapLineSceneItem, self).hoverEnterEvent(event)
        self.parent.lock_vertical.emit(self.line().x1())

    def hoverLeaveEvent(self, event):
        super(VerticalSnapLineSceneItem, self).hoverLeaveEvent(event)
        self.parent.unlock_vertical.emit()


class SnapLine(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super(SnapLine, self).__init__(*args, **kwargs)
        self.points = []

    def add_point(self, point):
        self.points.append(point)


class HorizontalSnapLine(SnapLine):

    lock_horizontal = QtCore.pyqtSignal(float)
    unlock_horizontal = QtCore.pyqtSignal()

    def __init__(self, rect, y, *args, **kwargs):
        super(HorizontalSnapLine, self).__init__(*args, **kwargs)
        self.y = y
        self.rect = rect

    def scene_item(self):
        item = HorizontalSnapLineSceneItem(self.rect.left(), self.y, self.rect.right(), self.y)
        item.parent = self
        return item


class VerticalSnapLine(SnapLine):

    lock_vertical = QtCore.pyqtSignal(float)
    unlock_vertical = QtCore.pyqtSignal()

    def __init__(self, rect, x, *args, **kwargs):
        super(VerticalSnapLine, self).__init__(*args, **kwargs)
        self.x = x
        self.rect = rect

    def scene_item(self):
        item = VerticalSnapLineSceneItem(self.x, self.rect.top(), self.x, self.rect.bottom())
        item.parent = self
        return item
