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

from sympy.geometry import Point, Segment

from items.item import Item
from items.scene_items import CircleSceneItem
from items.scene_items.point_scene_item import CenterPoint, QuarterPoint


class CircleItem(Item):

    name = 'Circle'
    icon = 'images/commands/circle.png'

    def __init__(self, point1, point2, *args, **kwargs):
        super(CircleItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        self.center_point = CenterPoint()
        self.center_point.setPos(self.point1.x, self.point1.y)
        self.add_scene_item(self.center_point)

        radius_segment = Segment(self.point1, self.point2)
        radius = radius_segment.length

        self.circle = CircleSceneItem(radius)
        self.circle.setParentItem(self.center_point)

        self.top = QuarterPoint()
        self.top.setPos(0, radius)
        self.top.setParentItem(self.center_point)

        self.bottom = QuarterPoint()
        self.bottom.setPos(0, -radius)
        self.bottom.setParentItem(self.center_point)

        self.left = QuarterPoint()
        self.left.setPos(-radius, 0)
        self.left.setParentItem(self.center_point)

        self.right = QuarterPoint()
        self.right.setPos(radius, 0)
        self.right.setParentItem(self.center_point)
