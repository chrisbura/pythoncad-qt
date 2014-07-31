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

from math import sqrt

from PyQt4 import QtGui

from items import Item, PointItem
from items.scene_items import PointSceneItem
from items.scene_items.scene_item import DefaultPenMixin


class CirclePreviewSceneItem(DefaultPenMixin, QtGui.QGraphicsEllipseItem):
    pass


class CircleScenePreview(Item):
    def __init__(self, point, *args, **kwargs):
        super(CircleScenePreview, self).__init__(*args, **kwargs)

        self.center_point = point
        self.center_point_item = PointItem(self.center_point)
        self.add_child_item(self.center_point_item)

        self.circle_item = CirclePreviewSceneItem(0, 0, 0, 0)
        self.add_scene_item(self.circle_item)

    def update(self, x, y):
        distance_x = self.center_point.x - x
        distance_y = self.center_point.y - y
        radius = sqrt(distance_x ** 2 + distance_y ** 2)
        diameter = radius * 2.0

        self.circle_item.setRect(
            self.center_point.x - radius,
            self.center_point.y - radius,
            diameter,
            diameter
        )
