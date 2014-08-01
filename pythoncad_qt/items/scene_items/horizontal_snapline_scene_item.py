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

from items.scene_items.snapline_scene_item import SnaplineSceneItem


class HorizontalSnaplineSceneItem(SnaplineSceneItem):

    def hover_enter_event(self, event):
        super(HorizontalSnaplineSceneItem, self).hover_enter_event(event)
        self.parent.lock_horizontal.emit(self.line().y1())

    def hover_leave_event(self, event):
        super(HorizontalSnaplineSceneItem, self).hover_leave_event(event)
        self.parent.unlock_horizontal.emit()

    def hover_move_event(self, event):
        super(HorizontalSnaplineSceneItem, self).hover_move_event(event)
        self.parent.lock_horizontal.emit(self.line().y1())

    def update_line(self, scene_rect):
        self.setLine(scene_rect.left(), self.parent.point.y, scene_rect.right(), self.parent.point.y)
