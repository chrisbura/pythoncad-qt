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

from sympy.geometry import Segment

from items import Item
from items.scene_items import SegmentSceneItem
from items.scene_items.point_scene_item import EndPoint, MidPoint


class SegmentItem(Item):
    def __init__(self, point1, point2, *args, **kwargs):
        super(SegmentItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        self.segment = Segment(self.point1, self.point2)

        # Segment
        self.segment_item = SegmentSceneItem(self.point1, self.point2)
        self.add_child(self.segment_item)

        # Start Point
        self.point1_item = EndPoint(self.point1)
        self.add_child(self.point1_item)

        # End Point
        self.point2_item = EndPoint(self.point2)
        self.add_child(self.point2_item)

        # Mid Point
        # TODO: Set deleteable = false
        # TODO: Set only visible on PointInput
        self.midpoint_item = MidPoint(self.segment.midpoint)
        self.add_child(self.midpoint_item)

    def horizontal_snap_points(self):
        return [self.point1.y, self.point2.y]

    def vertical_snap_points(self):
        return [self.point1.x, self.point2.x]
