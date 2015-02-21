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

from items import Item
from items.scene_items.snapline_scene_item import SnapGuideLine


class SnaplineItem(Item):
    def __init__(self, *args, **kwargs):
        super(SnaplineItem, self).__init__(*args, **kwargs)

        self.guide = SnapGuideLine()
        self.add_scene_item(self.guide)

        # Guide Line Signals
        self.line.hover_enter_signal.connect(self.show_guide)
        self.line.hover_leave_signal.connect(self.hide_guide)
        self.line.hover_move_signal.connect(self.update_guide)

        # Filter Signals
        self.line.hover_enter_signal.connect(self.activate_filters)
        self.line.hover_leave_signal.connect(self.deactivate_filters)

    def show_guide(self, event):
        self.guide.setVisible(True)

    def hide_guide(self, event):
        self.guide.setVisible(False)

    def set_guide(self, x1, y1, x2, y2):
        self.guide.setLine(x1, y1, x2, y2)

    def update_guide(self, event):
        pass
