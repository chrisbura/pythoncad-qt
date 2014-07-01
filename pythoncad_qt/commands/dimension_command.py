
from commands.base import Command
from commands.inputs import PointInput
from graphics_items.dimension_graphics_item import DimensionItem, VerticalDimensionItem, HorizontalDimensionItem

# TODO: Merge all 3 into one 'smart' dimension command


class DimensionCommand(Command):

    item = DimensionItem

    def __init__(self):
        super(DimensionCommand, self).__init__()

        self.has_preview = False
        self.preview_start = 0

        self.inputs = [
            PointInput('Enter First Point'),
            PointInput('Enter Second Point'),
            PointInput('Enter Third Point'),
        ]

    def preview_item(self):
        pass

    def apply_command(self):
        items = [
            self.item(
                self.inputs[0].value,
                self.inputs[1].value,
                self.inputs[2].value
            )
        ]
        return items

class VerticalDimensionCommand(DimensionCommand):
    item = VerticalDimensionItem


class HorizontalDimensionCommand(DimensionCommand):
    item = HorizontalDimensionItem
