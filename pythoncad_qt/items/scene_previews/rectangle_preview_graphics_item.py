
from PyQt4 import QtGui

from graphics_items.base_preview_graphics_item import BasePreviewGraphicsItem


class RectanglePreviewGraphicsItem(BasePreviewGraphicsItem):
    def __init__(self, point, *args, **kwargs):
        super(RectanglePreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.point = point
        self.lines = []

        for i in range(4):
            # Lines
            line = QtGui.QGraphicsLineItem()
            self.lines.append(line)

            # Add to QGraphicsItemGroup
            self.add_preview_item(line)

    def update(self, x, y):
        # Point Order is clockwise starting from initial point
        point1 = [self.point.x, self.point.y]
        point2 = [x, self.point.y]
        point3 = [x, y]
        point4 = [self.point.x, y]

        self.lines[0].setLine(*point1+point2)
        self.lines[1].setLine(*point2+point3)
        self.lines[2].setLine(*point3+point4)
        self.lines[3].setLine(*point4+point1)
