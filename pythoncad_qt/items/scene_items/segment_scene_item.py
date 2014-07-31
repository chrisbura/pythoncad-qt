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

from items.scene_items import SceneItem


class BaseSegmentSceneItem(SceneItem, QtGui.QGraphicsLineItem):
    def __init__(self, point1, point2):

        self.point1 = point1
        self.point2 = point2

        super(BaseSegmentSceneItem, self).__init__(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y)


class SegmentSceneItem(BaseSegmentSceneItem):

    def shape(self):
        p = QtGui.QPainterPath(QtCore.QPointF(self.point1.x, self.point1.y))
        p.lineTo(self.point2.x, self.point2.y)

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path
