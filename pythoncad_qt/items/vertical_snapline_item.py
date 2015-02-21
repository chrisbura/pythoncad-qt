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

from PyQt4 import QtGui, QtCore

from items.snapline_item import SnaplineItem
from items.scene_items.vertical_snapline_scene_item import VerticalSnaplineSceneItem
from input_filter import VerticalAxisLockFilter


class VerticalSnaplineItem(SnaplineItem):

    name = 'Vertical Snap Line'

    def __init__(self, scene_point, *args, **kwargs):

        self.scene_point = scene_point

        # Line dimensions will be set when added to scene
        self.line = VerticalSnaplineSceneItem(self.scene_point)
        super(VerticalSnaplineItem, self).__init__(*args, **kwargs)
        self.add_scene_item(self.line)

        self.filter = VerticalAxisLockFilter(self.scene_point.scenePos().x())
        self.scene_point.position_changed.connect(self.update_filter)
        self.add_filter(self.filter)

    def update_guide(self, event):
        point = self.scene_point.scenePos()
        self.set_guide(point.x(), point.y(), point.x(), event.y)

    def update_filter(self, *args, **kwargs):
        self.filter.set_value(self.scene_point.scenePos().x())
