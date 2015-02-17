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

from functools import partial

from sympy.geometry import Point

from commands.command import Command
from commands.inputs import CoordinateInput
from items import CircleItem
from items.scene_previews import CircleScenePreview


class CircleCommand(Command):
    def __init__(self, *args, **kwargs):
        super(CircleCommand, self).__init__(*args, **kwargs)

        self.preview_item = None

        # Start Point
        self.point1 = CoordinateInput()
        self.add_input(self.point1)

        # End Point
        self.point2 = CoordinateInput()
        self.add_input(self.point2)

        self.point1.input_valid.connect(self.add_preview)
        self.command_finished.connect(self.add_item)

    def add_preview(self):
        self.preview_item = CircleScenePreview(Point(self.point1.x, self.point1.y))
        self.mouse_received.connect(self.preview_item.update)
        self.command_finished.connect(partial(self.item_remove.emit, self.preview_item))
        self.command_cancelled.connect(partial(self.item_remove.emit, self.preview_item))
        self.item_ready.emit(self.preview_item)

    def add_item(self):
        item = CircleItem(
            Point(self.point1.x, self.point1.y),
            Point(self.point2.x, self.point2.y))
        self.item_ready.emit(item)
