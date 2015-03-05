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

import sip
from PyQt4 import QtGui, QtCore

from items.scene_items import SceneItem
from items.scene_items.point_scene_item import EndPoint


class SegmentEndPointSceneItem(EndPoint):
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged and self.scene():
            self.parentItem().update()

        # itemChange and setParentItem causes error in PyQt4
        # TODO: Test with PySide and PyQt5
        # See http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        result =  super(SegmentEndPointSceneItem, self).itemChange(change, value)
        if isinstance(result, QtGui.QGraphicsItem):
            result = sip.cast(result, QtGui.QGraphicsItem)
        return result


class SegmentSceneItem(SceneItem, QtGui.QGraphicsLineItem):
    def __init__(self, start, end, *args, **kwargs):
        super(SegmentSceneItem, self).__init__(*args, **kwargs)

        self.start = start
        self.end = end

    def shape(self):
        p = QtGui.QPainterPath(self.line().p1())
        p.lineTo(self.line().p2())

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path

    def paint(self, *args, **kwargs):
        line = QtCore.QLineF(self.start.pos(), self.end.pos())
        self.setLine(line)
        super(SegmentSceneItem, self).paint(*args, **kwargs)
