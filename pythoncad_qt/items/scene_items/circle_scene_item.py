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


class CircleSceneItem(SceneItem, QtGui.QGraphicsEllipseItem):
    def __init__(self, radius, *args, **kwargs):
        self.radius = radius
        diameter = self.radius * 2.0

        self.shape_cache = None

        super(CircleSceneItem, self).__init__(
            self.radius * -1.0,
            self.radius * -1.0,
            diameter,
            diameter
        )

    def shape(self):
        # Cache the shape call so that we don't recaulate the stroke unless it
        # changes
        # TODO: Invalidate cache when geometry changes
        if not self.shape_cache:
            shape = super(CircleSceneItem, self).shape()
            stroker = QtGui.QPainterPathStroker()
            stroker.setWidth(10.0)
            # simplified removes the 2 extra paths from the three (inside radius,
            # center, and outside radius)
            self.shape_cache = stroker.createStroke(shape).simplified()
        return self.shape_cache
