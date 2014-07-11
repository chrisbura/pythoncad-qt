
from items import Item
from items.scene_items import PointSceneItem
from graphics_items.snap_lines import HorizontalSnap, VerticalSnap

class PointItem(Item):
    def __init__(self, point, *args, **kwargs):
        super(PointItem, self).__init__(*args, **kwargs)

        self.point_item = PointSceneItem(point)
        self.add_child(self.point_item)

        self.horizontal_snap = HorizontalSnap(point)
        self.add_child(self.horizontal_snap)

        self.vertical_snap = VerticalSnap(point)
        self.add_child(self.vertical_snap)
