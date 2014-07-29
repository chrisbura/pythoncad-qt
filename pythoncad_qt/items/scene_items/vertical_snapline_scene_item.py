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


class VerticalSnaplineSceneItem(SnaplineSceneItem):
    def hoverEnterEvent(self, event):
        super(VerticalSnaplineSceneItem, self).hoverEnterEvent(event)
        self.parent.lock_vertical.emit(self.line().x1())

    def hoverLeaveEvent(self, event):
        super(VerticalSnaplineSceneItem, self).hoverLeaveEvent(event)
        self.parent.unlock_vertical.emit()

    def update_line(self, scene_rect):
        self.setLine(self.parent.point.x, scene_rect.top(), self.parent.point.x, scene_rect.bottom())