
from commands.base import Command
from commands.inputs import PointInput
from graphics_items.point_graphics_item import PointItem


class PointCommand(Command):
    def __init__(self):
        super(PointCommand, self).__init__()

        self.inputs = [
            PointInput('Enter Point'),
        ]

    def apply_command(self):
        return [PointItem(self.inputs[0].value)]
