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

from items.item import Item
from items.scene_previews.dimension_scene_preview import BaseDimensionScenePreview


class HorizontalDimensionScenePreview(BaseDimensionScenePreview):
    def update(self, x, y):

        self.lines[0].setLine(
            self.point1.x, self.point1.y,
            self.point1.x, y
        )

        self.lines[1].setLine(
            self.point2.x, self.point2.y,
            self.point2.x, y
        )

        self.lines[2].setLine(
            self.point1.x, y,
            self.point2.x, y
        )
