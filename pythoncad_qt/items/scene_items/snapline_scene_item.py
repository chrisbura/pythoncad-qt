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

import settings
from hover_event_manager import HoverEnterEvent, HoverLeaveEvent, HoverMoveEvent

class SnaplineSceneItem(QtGui.QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super(SnaplineSceneItem, self).__init__(*args, **kwargs)

        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.transparent)

        pen.setWidth(1)
        self.setPen(pen)
        self.setZValue(-100)

        self.setAcceptHoverEvents(True)

    def shape(self):
        p = QtGui.QPainterPath(self.line().p1())
        p.lineTo(self.line().p2())

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(15.0)
        path = stroker.createStroke(p)

        return path

    def paint(self, painter, option, widget):
        if settings.DEBUG_SNAP_LINES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())
        super(SnaplineSceneItem, self).paint(painter, option, widget)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSceneChange and value is not None:
            self.update_line(value.sceneRect())
        return super(SnaplineSceneItem, self).itemChange(change, value)

    def hover_event(self, event):
        if type(event) == HoverEnterEvent:
            self.hover_enter_event(event)

        if type(event) == HoverLeaveEvent:
            self.hover_leave_event(event)

        if type(event) == HoverMoveEvent:
            self.hover_move_event(event)

    def hover_enter_event(self, event):
        pen = self.pen()
        pen.setColor(QtCore.Qt.cyan)
        self.setPen(pen)

    def hover_leave_event(self, event):
        pen = self.pen()
        pen.setColor(QtCore.Qt.transparent)
        self.setPen(pen)

    def hover_move_event(self, event):
        pass
