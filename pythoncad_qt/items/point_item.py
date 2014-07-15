
from items import Item
from items.scene_items import PointSceneItem

class PointItem(Item):
    def __init__(self, point, *args, **kwargs):
        super(PointItem, self).__init__(*args, **kwargs)

        self.point = point

        self.point_item = PointSceneItem(point)
        self.add_child(self.point_item)

    def horizontal_snap_points(self):
        return [self.point.y]

    def vertical_snap_points(self):
        return [self.point.x]
