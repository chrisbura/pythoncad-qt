
from PyQt4 import QtGui, QtCore

import settings
from items.scene_items import SceneItem
from items.scene_items.scene_item import FilledShapeMixin


class PointSceneItem(FilledShapeMixin, SceneItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, point):
        self.entity = point
        self.radius = 2.0
        self.diameter = self.radius * 2.0

        self.shape_cache = None

        super(PointSceneItem, self).__init__(
            self.entity.x - self.radius,
            self.entity.y - self.radius,
            self.diameter,
            self.diameter)

    def shape(self):
        # TODO: Find how to properly handle overzealous shape calculations
        if not self.shape_cache:
            path = QtGui.QPainterPath()
            width = 20.0
            path.addEllipse(self.entity.x - width / 2.0, self.entity.y - width / 2.0, width, width)
            self.shape_cache = path
        return self.shape_cache

    def set_position(self, point):
        self.entity = point

        # Invalidate shape cache
        self.shape_cache = None

        # Args - x, y, w, h
        self.setRect(
            self.entity.x - self.radius,
            self.entity.y - self.radius,
            self.diameter, self.diameter
        )

    def hoverEnterEvent(self, event):
        super(PointSceneItem, self).hoverEnterEvent(event)
        self.parent.hover_enter.emit(self.entity)

    def hoverLeaveEvent(self, event):
        super(PointSceneItem, self).hoverLeaveEvent(event)
        self.parent.hover_leave.emit()


class SnapPoint(PointSceneItem):
    default_colour = QtCore.Qt.transparent
    hover_colour = QtCore.Qt.transparent

    def __init__(self, *args, **kwargs):
        super(SnapPoint, self).__init__(*args, **kwargs)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)


class MidPoint(SnapPoint):
    pass


class EndPoint(SnapPoint):
    pass


class CenterPoint(SnapPoint):
    pass


class QuarterPoint(SnapPoint):
    pass
