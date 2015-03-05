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

from items.scene_items.horizontal_snapline_scene_item import HorizontalSnaplineSceneItem, HorizontalSnapGuideLine
from items.scene_items.vertical_snapline_scene_item import VerticalSnaplineSceneItem, VerticalSnapGuideLine


class SnaplineItem(object):
    def __init__(self, point, *args, **kwargs):
        super(SnaplineItem, self).__init__(*args, **kwargs)

        self.vertical = VerticalSnaplineSceneItem(point)
        self.vertical_guide = VerticalSnapGuideLine(self.vertical)
        self.vertical.hover_enter_signal.connect(self.vertical_guide.show_guide)
        self.vertical.hover_move_signal.connect(self.vertical_guide.update_guide)
        self.vertical.hover_leave_signal.connect(self.vertical_guide.hide_guide)

        self.horizontal = HorizontalSnaplineSceneItem(point)
        self.horizontal_guide = HorizontalSnapGuideLine(self.horizontal)
        self.horizontal.hover_enter_signal.connect(self.horizontal_guide.show_guide)
        self.horizontal.hover_move_signal.connect(self.horizontal_guide.update_guide)
        self.horizontal.hover_leave_signal.connect(self.horizontal_guide.hide_guide)
