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

from sympy.geometry import Point

from commands.command import Command
from commands.inputs import PointInput
from items import SegmentItem
from items.scene_previews import RectangleScenePreview


class RectangleCommand(Command):
    def __init__(self):
        super(RectangleCommand, self).__init__()

        self.has_preview = True
        self.preview_start = 0

        self.inputs = [
            PointInput('Enter First Point'),
            PointInput('Enter Second Point'),
        ]

    def preview_item(self):
        return RectangleScenePreview(self.inputs[0].value)

    def apply_command(self):
        point1 = self.inputs[0].value
        point2 = self.inputs[1].value
        point3 = Point(point1.x, point2.y)
        point4 = Point(point2.x, point1.y)

        items = [
            SegmentItem(point1, point4),
            SegmentItem(point4, point2),
            SegmentItem(point2, point3),
            SegmentItem(point3, point1),
        ]

        return items
