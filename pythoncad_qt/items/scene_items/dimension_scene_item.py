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
