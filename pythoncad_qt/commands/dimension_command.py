
from commands.base import Command
from commands.inputs import PointInput
from graphics_items.dimension_graphics_item import DimensionItem, VerticalDimensionItem, HorizontalDimensionItem
from graphics_items.dimension_preview_graphics_item import DimensionPreviewGraphicsItem

# TODO: Merge all 3 into one 'smart' dimension command


class DimensionCommand(Command):

    item = DimensionItem

    def __init__(self):
        super(DimensionCommand, self).__init__()

        self.has_preview = True
        self.preview_start = 1

        self.inputs = [
            PointInput('Enter First Point'),
            PointInput('Enter Second Point'),
            PointInput('Enter Third Point'),
        ]

    def preview_item(self):
        return DimensionPreviewGraphicsItem(self.inputs[0].value, self.inputs[1].value)

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
