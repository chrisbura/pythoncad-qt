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

from items.scene_items import SceneItem


class SegmentSceneItem(SceneItem, QtGui.QGraphicsLineItem):
    def __init__(self, start_point, end_point, *args, **kwargs):
        super(SegmentSceneItem, self).__init__(*args, **kwargs)

        self.start_point = start_point
        self.end_point = end_point

        self.start_point.position_changed.connect(self.update_line)
        self.end_point.position_changed.connect(self.update_line)

    def shape(self):
        p = QtGui.QPainterPath(self.line().p1())
        p.lineTo(self.line().p2())

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path

    def update_line(self, *args, **kwargs):
        line = QtCore.QLineF(
            self.mapFromItem(self.start_point, 0, 0),
            self.mapFromItem(self.end_point, 0, 0))
        self.setLine(line)
