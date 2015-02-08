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

from sympy.geometry import Point, Segment

from items.scene_items import SceneItem


class DimensionSceneItem(SceneItem, QtGui.QGraphicsPathItem):
    default_colour = QtCore.Qt.gray
    hover_colour = QtCore.Qt.blue

    def __init__(self, *args, **kwargs):
        super(DimensionSceneItem, self).__init__(*args, **kwargs)
        # Want all the dimension segments to be behind other items
        self.setZValue(-1)

    def shape(self):
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(self.path())
        return path

    # TODO(chrisbura): Move to SceneItem (or mixins)
    def bring_to_front(self):
        self.setZValue(100)

    # TODO(chrisbura): Move to SceneItem (or mixins)
    def send_to_back(self):
        self.setZValue(-1)

    def hover_enter_event(self, event):
        super(DimensionSceneItem, self).hover_enter_event(event)
        # Bring the dimension item to the top when hovered
        # TODO(chrisbura): Define levels for each type of item
        # TODO(chrisbura): Add priority system for cycling thru hovered items
        self.bring_to_front()

    def hover_leave_event(self, event):
        super(DimensionSceneItem, self).hover_leave_event(event)
        # If we selected the item during hover event then don't send it back
        if not self.isSelected():
            self.send_to_back()

    def on_selected(self):
        super(DimensionSceneItem, self).on_selected()
        self.bring_to_front()

    def on_unselected(self):
        super(DimensionSceneItem, self).on_unselected()
        self.send_to_back()
