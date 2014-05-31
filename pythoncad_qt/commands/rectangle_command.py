
from sympy.geometry import Point

from commands.base import Command
from commands.inputs import PointInput
from graphics_items.segment_graphics_item import SegmentItem
from graphics_items.rectangle_preview_graphics_item import RectanglePreviewGraphicsItem


class RectangleCommand(Command):
    def __init__(self):
        super(RectangleCommand, self).__init__()

        self.has_preview = True
        self.preview_start = 0

        self.inputs = [
            PointInput('Enter First Point'),
            PointInput('Enter Second Point'),
        ]

    def preview_item(self):
        return RectanglePreviewGraphicsItem(self.inputs[0].value)

    def apply_command(self):
        point1 = self.inputs[0].value
        point2 = self.inputs[1].value
        point3 = Point(point1.x, point2.y)
        point4 = Point(point2.x, point1.y)

        items = [
            SegmentItem(point1, point4),
            SegmentItem(point4, point2),
            SegmentItem(point2, point3),
            SegmentItem(point3, point1),
        ]

        return items
