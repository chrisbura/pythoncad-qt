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

from items import Item
from items.scene_items import PointSceneItem
from items.scene_items.point_scene_item import EndPoint, CenterPoint, MidPoint, QuarterPoint
from items.vertical_snapline_item import VerticalSnaplineItem
from items.horizontal_snapline_item import HorizontalSnaplineItem


class PointSnaplines(object):
    def __init__(self, *args, **kwargs):
        super(PointSnaplines, self).__init__(*args, **kwargs)

        self.horizontal_snapline = HorizontalSnaplineItem(self.point)
        self.vertical_snapline = VerticalSnaplineItem(self.point)
        self.add_item(self.horizontal_snapline)
        self.add_item(self.vertical_snapline)


class PointItem(PointSnaplines, Item):
    def __init__(self, point, *args, **kwargs):
        self.point = point
        super(PointItem, self).__init__(*args, **kwargs)
        self.point_item = PointSceneItem(point)
        self.add_child(self.point_item)

    def horizontal_snap_points(self):
        return [self.point.y]

    def vertical_snap_points(self):
        return [self.point.x]


class EndPointItem(PointSnaplines, Item):
    def __init__(self, point, *args, **kwargs):
        self.point = point
        super(EndPointItem, self).__init__(*args, **kwargs)
        self.point_item = EndPoint(self.point)
        self.add_child(self.point_item)
