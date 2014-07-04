
from PyQt4 import QtGui

from graphics_items.base_preview_graphics_item import BasePreviewGraphicsItem
from graphics_items.point_graphics_item import PointGraphicsItem


class RectanglePreviewGraphicsItem(BasePreviewGraphicsItem):
    def __init__(self, point, *args, **kwargs):
        super(RectanglePreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.point = point
        self.lines = []
        self.points = []

        for i in range(4):
            # Lines
            line = QtGui.QGraphicsLineItem()
            self.lines.append(line)

            # Points
            point = PointGraphicsItem(self.point)
            self.points.append(point)

            # Add to QGraphicsItemGroup
            self.add_preview_item(line)
            self.add_preview_item(point)

    def update(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()

        # Point Order is clockwise starting from initial point
        point1 = [self.point.x, self.point.y]
        point2 = [x, self.point.y]
        point3 = [x, y]
        point4 = [self.point.x, y]

        self.lines[0].setLine(*point1+point2)
        self.lines[1].setLine(*point2+point3)
        self.lines[2].setLine(*point3+point4)
        self.lines[3].setLine(*point4+point1)

        # self.points[0] doesn't change
        # self.points[2] is current mouse position

        # TODO: Create points class for previews (without shape calculations)
        self.points[1].setRect(
            point2[0] - self.points[1].radius,
            point2[1] - self.points[1].radius,
            self.points[1].radius * 2,
            self.points[1].radius * 2
        )
        self.points[3].setRect(
            point4[0] - self.points[3].radius,
            point4[1] - self.points[3].radius,
            self.points[3].radius * 2,
            self.points[3].radius * 2
        )
