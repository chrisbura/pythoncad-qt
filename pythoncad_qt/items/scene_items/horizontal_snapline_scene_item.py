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

from items.scene_items.snapline_scene_item import SnaplineSceneItem


class HorizontalSnaplineSceneItem(SnaplineSceneItem):
    def paint(self, painter, option, widget):
        rect = self.scene().sceneRect()

        left = self.mapFromScene(rect.left(), 0).x()
        right = self.mapFromScene(rect.right(), 0).x()

        line = QtCore.QLineF(left, 0, right, 0)
        self.setLine(line)
        super(HorizontalSnaplineSceneItem, self).paint(painter, option, widget)

    def snap_coordinate(self, value):
        value.setY(self.parentItem().scenePos().y())
        return value
