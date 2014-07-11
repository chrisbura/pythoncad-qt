
from sympy.geometry import Point

from items import Item
from items.scene_items import CircleSceneItem
from items.scene_items.point_scene_item import CenterPoint, QuarterPoint

class CircleItem(Item):
    def __init__(self, point1, point2, *args, **kwargs):
        super(CircleItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        circle_item = CircleSceneItem(self.point1, self.point2)
        self.add_child(circle_item)

        # Snap Points
        center_point_item = CenterPoint(self.point1)
        self.add_child(center_point_item)

        quarter_points = [
            Point(self.point1.x, self.point1.y + circle_item.radius),
            Point(self.point1.x, self.point1.y - circle_item.radius),
            Point(self.point1.x + circle_item.radius, self.point1.y),
            Point(self.point1.x - circle_item.radius, self.point1.y)
        ]

        for point in quarter_points:
            self.add_child(QuarterPoint(point))
