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

from items import Item, PointItem
from items.scene_items import SegmentSceneItem
from items.point_item import EndPointItem
from items.scene_items.point_scene_item import EndPoint, MidPoint


class SegmentItem(Item):

    name = 'Segment'
    icon = 'images/commands/segment.png'

    def __init__(self, point1, point2, *args, **kwargs):
        super(SegmentItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        self.segment = Segment(self.point1, self.point2)

        # Segment
        self.segment_item = SegmentSceneItem(self.point1, self.point2)
        self.add_scene_item(self.segment_item)

        # Start Point
        self.point1_item = EndPointItem(self.point1)
        self.add_child_item(self.point1_item)

        # End Point
        self.point2_item = EndPointItem(self.point2)
        self.add_child_item(self.point2_item)

        # Mid Point
        # TODO: Set deleteable = false
        # TODO: Set only visible on PointInput
        self.midpoint_item = MidPoint(self.segment.midpoint)
        self.add_scene_item(self.midpoint_item)
