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

from items.scene_items.snapline_scene_item import SnaplineSceneItem, SnapGuideLine


# TODO: Have guide use internal
class VerticalSnaplineSceneItem(SnaplineSceneItem):
    def paint(self, painter, option, widget):
        rect = self.scene().sceneRect()

        top = self.mapFromScene(0, rect.top()).y()
        bottom = self.mapFromScene(0, rect.bottom()).y()

        line = QtCore.QLineF(0, top, 0, bottom)
        self.setLine(line)
        super(VerticalSnaplineSceneItem, self).paint(painter, option, widget)

    def snap_coordinate(self, value):
        value.setX(self.parentItem().scenePos().x())
        return value


class VerticalSnapGuideLine(SnapGuideLine):
    def update_guide(self, event):
        point = self.mapFromScene(event.scenePos())
        line = QtCore.QLineF(0, 0, 0, point.y())
        self.setLine(line)
