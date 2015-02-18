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

import settings
from hover_event_manager import HoverState
from items.scene_items.simple_signal import SimpleSignal


class SnapGuidePen(QtGui.QPen):
    """
    SnapGuidePen is used for the primary active guide which is usually from the
    closest point.
    """
    colour = settings.SNAP_GUIDE_COLOUR
    style = settings.SNAP_GUIDE_STYLE

    def __init__(self, *args, **kwargs):
        super(SnapGuidePen, self).__init__(*args, **kwargs)
        self.setWidth(2)
        self.setColor(self.colour)
        self.setStyle(self.style)


class SnapGuideSecondaryPen(SnapGuidePen):
    colour = settings.SNAP_GUIDE_SECONDARY_COLOUR


class SnapGuideLine(QtGui.QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super(SnapGuideLine, self).__init__(*args, **kwargs)
        self.setVisible(False)
        self.setPen(SnapGuidePen())


class SnaplineSceneItem(HoverState, QtGui.QGraphicsLineItem):

    def __init__(self, *args, **kwargs):
        super(SnaplineSceneItem, self).__init__(*args, **kwargs)

        self.default_pen = QtGui.QPen(QtCore.Qt.transparent)
        self.default_pen.setWidth(1)

        self.hover_pen = QtGui.QPen(QtCore.Qt.cyan)
        self.hover_pen.setWidth(1)

        self.setPen(self.default_pen)
        self.setZValue(-100)

        self.setAcceptHoverEvents(True)

        self.hover_enter_signal = SimpleSignal()
        self.hover_leave_signal = SimpleSignal()
        self.hover_move_signal = SimpleSignal()

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

    def hover_enter_event(self, event):
        # TODO(chrisbura): Get rid of event.event...
        self.hover_enter_signal.emit(event.event)

        if settings.DEBUG_SNAP_LINES:
            self.setPen(self.hover_pen)

    def hover_leave_event(self, event):
        # TODO(chrisbura): Get rid of event.event...
        self.hover_leave_signal.emit(event.event)

        if settings.DEBUG_SNAP_LINES:
            self.setPen(self.default_pen)

    def hover_move_event(self, event):
        # TODO(chrisbura): Get rid of event.event...
        self.hover_move_signal.emit(event.event)
