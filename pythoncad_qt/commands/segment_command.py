
from commands.base import Command
from commands.inputs import PointInput
from graphics_items.segment_graphics_item import SegmentItem
from graphics_items.segment_preview_graphics_item import SegmentPreviewGraphicsItem


class SegmentCommand(Command):
    def __init__(self):
        super(SegmentCommand, self).__init__()

        self.has_preview = True
        self.preview_start = 0

        self.inputs = [
            PointInput('Enter First Point'),
            PointInput('Enter Second Point'),
        ]

    def preview_item(self):
        return SegmentPreviewGraphicsItem(self.inputs[0].value)

    def apply_command(self):
        return [SegmentItem(self.inputs[0].value, self.inputs[1].value)]
