
from PyQt4 import QtCore

from sympy.geometry import Point

from graphics_items.point_graphics_item import PointGraphicsItem
from commands.inputs import PointInput


class Command(QtCore.QObject):

    command_ended = QtCore.pyqtSignal()
    command_cancelled = QtCore.pyqtSignal()
    add_item = QtCore.pyqtSignal(object)
    command_finished = QtCore.pyqtSignal(object)
    remove_item = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.values = []
        self.active_input = 0
        self.has_preview = False
        self.preview_start = 0
        self.preview_graphics_item = None

    def process_click(self, event, items):
        current_input = self.inputs[self.active_input]

        if isinstance(current_input, PointInput):
            # TODO: Handle multiple points
            items = [item for item in items if isinstance(item, PointGraphicsItem)]

            if items:
                current_input.value = Point(items[0].entity.x, items[0].entity.y)
            else:
                current_input.value = Point(event.scenePos().x(), event.scenePos().y())

        if self.has_preview and (self.active_input == self.preview_start):
            self.preview_graphics_item = self.preview_item()
            self.add_item.emit(self.preview_graphics_item)

        self.active_input = self.active_input + 1

        if self.active_input == len(self.inputs):
            graphics_items = self.apply_command()
            self.command_finished.emit(graphics_items)

            self.remove_preview_item()
            self.command_ended.emit()

    def process_move(self, event):
        if self.preview_graphics_item:
            self.preview_graphics_item.update(event)

    def cancel(self):
        self.remove_preview_item()
        self.command_cancelled.emit()

    def remove_preview_item(self):
        if self.preview_graphics_item is not None:
            self.remove_item.emit(self.preview_graphics_item)
            self.preview_graphics_item = None
