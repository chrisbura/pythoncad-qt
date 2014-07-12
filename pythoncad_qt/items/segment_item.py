
from sympy.geometry import Segment

from items import Item
from items.scene_items import SegmentSceneItem
from items.scene_items.point_scene_item import EndPoint, MidPoint
from graphics_items.snap_lines import HorizontalSnap, VerticalSnap


class SegmentItem(Item):
    def __init__(self, point1, point2, *args, **kwargs):
        super(SegmentItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        self.segment = Segment(self.point1, self.point2)

        # Segment
        self.segment_item = SegmentSceneItem(self.point1, self.point2)
        self.add_child(self.segment_item)

        # Start Point
        self.point1_item = EndPoint(self.point1)
        self.add_child(self.point1_item)

        self.horizontal_snap = HorizontalSnap(self.point1)
        self.add_child(self.horizontal_snap)

        self.vertical_snap = VerticalSnap(self.point1)
        self.add_child(self.vertical_snap)

        # End Point
        self.point2_item = EndPoint(self.point2)
        self.add_child(self.point2_item)

        self.horizontal_snap = HorizontalSnap(self.point2)
        self.add_child(self.horizontal_snap)

        self.vertical_snap = VerticalSnap(self.point2)
        self.add_child(self.vertical_snap)

        # Mid Point
        # TODO: Set deleteable = false
        # TODO: Set only visible on PointInput
        self.midpoint_item = MidPoint(self.segment.midpoint)
        self.add_child(self.midpoint_item)
