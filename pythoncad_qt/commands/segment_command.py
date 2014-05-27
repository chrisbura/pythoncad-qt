
from commands.base import Command
from commands.inputs import PointInput
from graphics_items.segment_graphics_item import SegmentGraphicsGroup


class SegmentCommand(Command):
    def __init__(self):
        super(SegmentCommand, self).__init__()

        self.inputs = [
            PointInput('Enter First Point'),
            PointInput('Enter Second Point'),
        ]

    def apply_command(self):
        return SegmentGraphicsGroup(self.inputs[0].value, self.inputs[1].value)
