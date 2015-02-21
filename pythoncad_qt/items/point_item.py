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
from items.scene_items import PointSceneItem
from items.scene_items.point_scene_item import EndPoint, CenterPoint, MidPoint, QuarterPoint, HiddenPoint
from items.vertical_snapline_item import VerticalSnaplineItem
from items.horizontal_snapline_item import HorizontalSnaplineItem


class BasePointItem(Item):

    name = 'Point'
    scene_item = PointSceneItem

    def __init__(self, point, *args, **kwargs):
        self.point = point
        super(BasePointItem, self).__init__(*args, **kwargs)

        self.point_item = self.scene_item(point)
        self.add_scene_item(self.point_item)

        self.horizontal_snapline = HorizontalSnaplineItem(self.point_item)
        self.add_child_item(self.horizontal_snapline)

        self.vertical_snapline = VerticalSnaplineItem(self.point_item)
        self.add_child_item(self.vertical_snapline)


class PointItem(BasePointItem):
    pass


class HiddenPointItem(BasePointItem):
    scene_item = HiddenPoint


class EndPointItem(BasePointItem):
    scene_item = EndPoint


class MidPointItem(BasePointItem):
    scene_item = MidPoint


class CenterPointItem(BasePointItem):
    scene_item = CenterPoint


class QuarterPointItem(BasePointItem):
    scene_item = QuarterPoint
