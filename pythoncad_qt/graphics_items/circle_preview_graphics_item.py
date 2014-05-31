
from PyQt4 import QtGui

from sympy.geometry import Point, Segment

from graphics_items.point_graphics_item import PointGraphicsItem
from graphics_items.circle_graphics_item import CircleGraphicsItem

# TODO: Investigate why it takes so much processing power


class CirclePreviewGraphicsItem(QtGui.QGraphicsItemGroup):
    def __init__(self, point, *args, **kwargs):
        super(CirclePreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.center_point = point
        self.center_point_item = PointGraphicsItem(self.center_point)
        self.addToGroup(self.center_point_item)

        self.circle_item = QtGui.QGraphicsEllipseItem(0, 0, 0, 0)
        self.addToGroup(self.circle_item)

    def update(self, event):
        point = Point(event.scenePos().x(), event.scenePos().y())
        radius_segment = Segment(self.center_point, point)
        radius = radius_segment.length
        diameter = radius * 2.0

        updated_circle = QtGui.QGraphicsEllipseItem(
            self.center_point.x - radius,
            self.center_point.y - radius,
            diameter,
            diameter

        )
        self.circle_item.setRect(updated_circle.rect())
