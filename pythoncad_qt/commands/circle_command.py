
from commands.command import Command
from commands.inputs import PointInput
from items import CircleItem
from items.scene_previews import CircleScenePreview


class CircleCommand(Command):
    def __init__(self):
        super(CircleCommand, self).__init__()

        self.has_preview = True
        self.preview_start = 0

        self.inputs = [
            PointInput('Enter Center Point'),
            PointInput('Enter Second Point'),
        ]

    def preview_item(self):
        return CircleScenePreview(self.inputs[0].value)

    def apply_command(self):
        return [CircleItem(self.inputs[0].value, self.inputs[1].value)]
