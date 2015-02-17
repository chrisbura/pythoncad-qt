#
# PythonCAD-Qt
# Copyright (C) 2014-2015 Christopher Bura
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

from sympy.geometry import Point

from commands.command import Command
from commands.inputs import CoordinateInput
from items import PointItem


class PointCommand(Command):
    def __init__(self, *args, **kwargs):
        super(PointCommand, self).__init__(*args, **kwargs)

        self.point_input = CoordinateInput()
        self.add_input(self.point_input)

        self.command_finished.connect(self.add_item)

    def add_item(self):
        item = PointItem(Point(self.point_input.x, self.point_input.y))
        self.item_ready.emit(item)
