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

from sympy.geometry import Segment

from items.item import Item
from items.scene_items.segment_scene_item import SegmentSceneItem, SegmentEndPointSceneItem
from items.point_item import MidPointItem
from items.snapline_item import SnaplineItem


class SegmentItem(Item):

    name = 'Segment'
    icon = 'images/commands/segment.png'

    def __init__(self, point1, point2, *args, **kwargs):
        super(SegmentItem, self).__init__(*args, **kwargs)

        self.point1 = point1
        self.point2 = point2

        self.segment = Segment(self.point1, self.point2)

        self.start = SegmentEndPointSceneItem()
        self.end = SegmentEndPointSceneItem()
        self.line = SegmentSceneItem(self.start, self.end)

        self.start.setParentItem(self.line)
        self.start.setPos(self.point1.x, self.point1.y)

        self.end.setParentItem(self.line)
        self.end.setPos(self.point2.x, self.point2.y)

        self.add_scene_item(self.line)

        self.start_snaplines = SnaplineItem(self.start)
        self.end_snaplines = SnaplineItem(self.end)

        # Mid Point
        # TODO: Set only visible on PointInput
        # self.midpoint_item = MidPointItem(self.segment.midpoint)
        # self.add_child_item(self.midpoint_item)
