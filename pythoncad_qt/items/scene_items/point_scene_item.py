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
from items.scene_items import SceneItem
from items.scene_items.scene_item import FilledShapeMixin, UnselectableMixin, CoordinateSnapMixin, MovableMixin


class PointSceneItem(CoordinateSnapMixin, MovableMixin, FilledShapeMixin, SceneItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        self.radius = 2.0
        self.diameter = self.radius * 2.0

        self.shape_cache = None

        super(PointSceneItem, self).__init__(
            self.radius * -1,
            self.radius * -1,
            self.diameter,
            self.diameter)

    def shape(self):
        # TODO: Find how to properly handle overzealous shape calculations
        if not self.shape_cache:
            path = QtGui.QPainterPath()
            width = 20.0
            path.addEllipse(-1 * width / 2.0, -1 * width / 2.0, width, width)
            self.shape_cache = path
        return self.shape_cache


class SnapPoint(UnselectableMixin, PointSceneItem):
    default_colour = QtCore.Qt.transparent
    hover_colour = QtCore.Qt.transparent

    def __init__(self, *args, **kwargs):
        super(SnapPoint, self).__init__(*args, **kwargs)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)


class MidPoint(SnapPoint):
    pass


class EndPoint(PointSceneItem):
    pass


class CenterPoint(SnapPoint):
    pass


class QuarterPoint(SnapPoint):
    pass


class HiddenPoint(SnapPoint):
    pass
