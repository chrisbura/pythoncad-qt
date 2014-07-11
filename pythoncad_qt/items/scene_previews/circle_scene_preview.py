from math import sqrt

from PyQt4 import QtGui

from items.scene_previews import ScenePreview
from items.scene_items import PointSceneItem


class CircleScenePreview(ScenePreview):
    def __init__(self, point, *args, **kwargs):
        super(CircleScenePreview, self).__init__(*args, **kwargs)

        self.center_point = point
        self.center_point_item = PointSceneItem(self.center_point)
        self.add_preview_item(self.center_point_item)

        self.circle_item = QtGui.QGraphicsEllipseItem(0, 0, 0, 0)
        self.add_preview_item(self.circle_item)

    def update(self, x, y):
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
