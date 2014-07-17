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

from items import Item
from items.scene_items import CircleSceneItem
from items.scene_items.point_scene_item import CenterPoint, QuarterPoint

class CircleItem(Item):
    def __init__(self, point1, point2, *args, **kwargs):
        super(CircleItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        circle_item = CircleSceneItem(self.point1, self.point2)
        self.add_child(circle_item)

        # Snap Points
        center_point_item = CenterPoint(self.point1)
        self.add_child(center_point_item)

        quarter_points = [
            Point(self.point1.x, self.point1.y + circle_item.radius),
            Point(self.point1.x, self.point1.y - circle_item.radius),
            Point(self.point1.x + circle_item.radius, self.point1.y),
            Point(self.point1.x - circle_item.radius, self.point1.y)
        ]

        for point in quarter_points:
            self.add_child(QuarterPoint(point))
