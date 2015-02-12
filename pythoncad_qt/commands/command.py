#
# PythonCAD-Qt
# Copyright (C) 2014 Christopher Bura
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from PyQt4 import QtCore

from sympy.geometry import Point

from items.scene_items import PointSceneItem
from commands.inputs import PointInput


class Command(QtCore.QObject):

    command_finished = QtCore.pyqtSignal(object)
    command_ended = QtCore.pyqtSignal()
    add_item = QtCore.pyqtSignal(object)
    remove_item = QtCore.pyqtSignal(object)
    add_preview = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.values = []
        self.active_input = 0
        self.has_preview = False
        self.preview_start = 0
        self.preview_graphics_item = None
        self.input_snapped = False

    def process_click(self, x, y, items):
        current_input = self.inputs[self.active_input]

        if isinstance(current_input, PointInput):
            # TODO: Handle multiple points
            # TODO(chrisbura): Ignore clicks on preview item when on snapline (try with rectangle and snapline)
            items = [item for item in items if isinstance(item, PointSceneItem)]

            if items:
                current_input.value = Point(items[0].entity.x, items[0].entity.y)
            else:
                current_input.value = Point(x, y)

        if self.has_preview and (self.active_input == self.preview_start):
            self.preview_graphics_item = self.preview_item()
            self.add_preview.emit(self.preview_graphics_item)

        self.active_input = self.active_input + 1

        if self.active_input == len(self.inputs):
            graphics_items = self.apply_command()
            self.command_finished.emit(graphics_items)
            self.cleanup()
            self.command_ended.emit()

    def snap_preview(self, point):
        self.input_snapped = True
        if self.preview_graphics_item:
            self.preview_graphics_item.update(point.x, point.y)

    def snap_release(self):
        self.input_snapped = False

    def process_move(self, x, y):
        if not self.input_snapped:
            if self.preview_graphics_item:
                self.preview_graphics_item.update(x, y)

    def cleanup(self):
        self.remove_preview_item()

    def remove_preview_item(self):
        if self.preview_graphics_item is not None:
            self.preview_graphics_item.delete.emit()
            self.preview_graphics_item = None
