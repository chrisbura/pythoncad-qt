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

from sympy.geometry import Point, Segment

from PyQt4 import QtGui, QtCore

from items import Item
from items.scene_items import DimensionSceneItem


class DimensionItem(Item):
    def __init__(self, point1, point2, point3, *args, **kwargs):
        super(DimensionItem, self).__init__(*args, **kwargs)

        # Create segment between the two points
        segment = Segment(point1, point2)

        # Get a line parallel to segment that passes through the third point
        parallel_line = segment.parallel_line(point3)

        # Get perpendicular segments from the points to the new parallel line
        perpendicular_line_p1 = parallel_line.perpendicular_segment(point1)
        perpendicular_line_p2 = parallel_line.perpendicular_segment(point2)

        # Order of XX.points from sympy changes if point3 is above or below
        # the segment, remove original point so we are left with new one
        perpendicular_line_p1_points = list(perpendicular_line_p1.points)
        perpendicular_line_p1_points.remove(point1)
        perpendicular_line_p2_points = list(perpendicular_line_p2.points)
        perpendicular_line_p2_points.remove(point2)

        # TODO: Refactor, code repeated 3 times
        self.path = QtGui.QPainterPath(QtCore.QPointF(point1.x, point1.y))
        self.path.lineTo(perpendicular_line_p1_points[0].x, perpendicular_line_p1_points[0].y)
        self.path.lineTo(perpendicular_line_p2_points[0].x, perpendicular_line_p2_points[0].y)
        self.path.lineTo(point2.x, point2.y)

        self.path_item = DimensionSceneItem(self.path)
        self.add_scene_item(self.path_item)

        self.text = QtGui.QGraphicsSimpleTextItem('{0}'.format(segment.length))
        self.text.setPos(point3.x, point3.y)
        # TODO: DocumentView.scale causes text to be flipped, need to get
        # proper mapping from scene
        self.text.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True)
        self.add_scene_item(self.text)


class VerticalDimensionItem(Item):
    def __init__(self, point1, point2, point3, *args, **kwargs):
        super(VerticalDimensionItem, self).__init__(*args, **kwargs)

        newp1 = Point(point3.x, point1.y)
        newp2 = Point(point3.x, point2.y)

        self.path = QtGui.QPainterPath(QtCore.QPointF(point1.x, point1.y))
        self.path.lineTo(newp1.x, newp1.y)
        self.path.lineTo(newp2.x, newp2.y)
        self.path.lineTo(point2.x, point2.y)

        self.path_item = DimensionSceneItem(self.path)
        self.add_scene_item(self.path_item)


class HorizontalDimensionItem(Item):
    def __init__(self, point1, point2, point3, *args, **kwargs):
        super(HorizontalDimensionItem, self).__init__(*args, **kwargs)

        newp1 = Point(point1.x, point3.y)
        newp2 = Point(point2.x, point3.y)

        self.path = QtGui.QPainterPath(QtCore.QPointF(point1.x, point1.y))
        self.path.lineTo(newp1.x, newp1.y)
        self.path.lineTo(newp2.x, newp2.y)
        self.path.lineTo(point2.x, point2.y)

        self.path_item = DimensionSceneItem(self.path)
        self.add_scene_item(self.path_item)
