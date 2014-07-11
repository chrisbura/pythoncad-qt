from PyQt4 import QtGui, QtCore

from sympy.geometry import Segment

from items.scene_items import SceneItem


class CircleSceneItem(SceneItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, point1, point2):

        self.shape_cache = None

        self.point1 = point1
        self.point2 = point2

        radius_segment = Segment(self.point1, self.point2)
        self.radius = radius_segment.length
        diameter = self.radius * 2.0

        super(CircleSceneItem, self).__init__(
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
            shape = super(CircleSceneItem, self).shape()
            stroker = QtGui.QPainterPathStroker()
            stroker.setWidth(10.0)
            # simplified removes the 2 extra paths from the three (inside radius,
            # center, and outside radius)
            self.shape_cache = stroker.createStroke(shape).simplified()
        return self.shape_cache
