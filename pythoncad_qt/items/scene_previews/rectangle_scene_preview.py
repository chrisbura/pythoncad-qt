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

from PyQt4 import QtGui

from items import Item
from items.scene_items.scene_item import DefaultPenMixin


class RectanglePreviewLineItem(DefaultPenMixin, QtGui.QGraphicsLineItem):
    pass


class RectangleScenePreview(Item):
    def __init__(self, point, *args, **kwargs):
        super(RectangleScenePreview, self).__init__(*args, **kwargs)

        self.point = point
        self.lines = []

        for i in range(4):
            # Lines
            line = RectanglePreviewLineItem()
            self.lines.append(line)
            self.add_scene_item(line)

    def update(self, x, y):
        # Point Order is clockwise starting from initial point
        point1 = [self.point.x, self.point.y]
        point2 = [x, self.point.y]
        point3 = [x, y]
        point4 = [self.point.x, y]

        self.lines[0].setLine(*point1+point2)
        self.lines[1].setLine(*point2+point3)
        self.lines[2].setLine(*point3+point4)
        self.lines[3].setLine(*point4+point1)
