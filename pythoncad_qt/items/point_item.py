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
from items.scene_items.horizontal_snapline_scene_item import HorizontalSnaplineSceneItem
from items.scene_items.vertical_snapline_scene_item import VerticalSnaplineSceneItem


class BasePointItem(Item):

    name = 'Point'
    scene_item = PointSceneItem

    def __init__(self, point, *args, **kwargs):
        self.point = point
        super(BasePointItem, self).__init__(*args, **kwargs)

        self.point_item = self.scene_item()
        self.point_item.setPos(self.point.x, self.point.y)
        self.add_scene_item(self.point_item)

        self.horizontal_snapline = HorizontalSnaplineSceneItem(self.point_item)
        self.vertical_snapline = VerticalSnaplineSceneItem(self.point_item)


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
