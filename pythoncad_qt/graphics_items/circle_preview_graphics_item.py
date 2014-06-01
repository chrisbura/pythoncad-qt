from math import sqrt

from PyQt4 import QtGui

from graphics_items.point_graphics_item import PointGraphicsItem


class CirclePreviewGraphicsItem(QtGui.QGraphicsItemGroup):
    def __init__(self, point, *args, **kwargs):
        super(CirclePreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.center_point = point
        self.center_point_item = PointGraphicsItem(self.center_point)
        self.addToGroup(self.center_point_item)

        self.circle_item = QtGui.QGraphicsEllipseItem(0, 0, 0, 0)
        self.addToGroup(self.circle_item)

    def update(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()

        distance_x = self.center_point.x - x
        distance_y = self.center_point.y - y
        radius = sqrt(distance_x ** 2 + distance_y ** 2)
        diameter = radius * 2.0

        self.circle_item.setRect(
            self.center_point.x - radius,
            self.center_point.y - radius,
            diameter,
            diameter
        )
