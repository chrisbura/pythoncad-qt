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

from PyQt4 import QtGui, QtCore

from items.snapline_item import SnaplineItem
from items.scene_items.horizontal_snapline_scene_item import HorizontalSnaplineSceneItem


class HorizontalSnaplineItem(SnaplineItem):
    def __init__(self, point, *args, **kwargs):
        super(HorizontalSnaplineItem, self).__init__(*args, **kwargs)
        self.point = point
        # Line dimensions will be set when added to scene
        self.line = HorizontalSnaplineSceneItem()
        self.add_child(self.line)
