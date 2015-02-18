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

from sympy.geometry import Point, Segment

from PyQt4 import QtGui, QtCore

from items import Item
from items.scene_items import DimensionSceneItem
from items.scene_items.text_scene_item import TextSceneItem
from items.point_item import HiddenPointItem


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

        new_segment = Segment(perpendicular_line_p1_points[0], perpendicular_line_p2_points[0])
        midpoint = new_segment.midpoint

        segment_midpoint = segment.midpoint

        # TODO: Customizable precision
        self.text_item = TextSceneItem('{0:.2f}'.format(float(segment.length.evalf())))
        self.text_item.setTransform(self.text_item.sceneTransform().scale(1, -1))
        self.add_scene_item(self.text_item)

        bounding_rect = self.text_item.boundingRect()
        offset_x = 0
        offset_y = 0

        # Quadrant 1, 4, Horizontal Right
        if midpoint.x > segment_midpoint.x:
            offset_x = bounding_rect.width() / 2

        # Quadrant 2, 3, Horizontal Left
        if midpoint.x < segment_midpoint.x:
            offset_x = -bounding_rect.width() / 2

        # Quadrant 1, 2, Vertical Top
        if midpoint.y > segment_midpoint.y:
            offset_y = bounding_rect.height() / 2

        # Quadrant 3, 4, Vertical Bottom
        if midpoint.y < segment_midpoint.y:
            offset_y = -bounding_rect.height() / 2

        self.text_item.setPos(midpoint.x + offset_x, midpoint.y + offset_y)

        # Point used to allow alligning dimension labels
        point_item = HiddenPointItem(midpoint)
        self.add_child_item(point_item)


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

        # TODO: Repeated for all dimension items
        # Determine where to place label
        segment = Segment(point1, point2)
        segment_midpoint = segment.midpoint

        # Get length
        new_segment = Segment(newp1, newp2)
        midpoint = new_segment.midpoint

        # TODO: Customizable precision
        self.text_item = TextSceneItem('{0:.2f}'.format(float(new_segment.length.evalf())))
        self.text_item.setTransform(self.text_item.sceneTransform().scale(1, -1))
        self.add_scene_item(self.text_item)

        bounding_rect = self.text_item.boundingRect()
        offset_x = 0
        offset_y = 0

        # Horizontal Right
        if midpoint.x > segment_midpoint.x:
            offset_x = bounding_rect.width() / 2

        # Horizontal Left
        if midpoint.x < segment_midpoint.x:
            offset_x = -bounding_rect.width() / 2

        self.text_item.setPos(midpoint.x + offset_x, midpoint.y + offset_y)

        # Point used to allow alligning dimension labels
        point_item = HiddenPointItem(midpoint)
        self.add_child_item(point_item)


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

        # TODO: Repeated for all dimension items
        # Determine where to place label
        segment = Segment(point1, point2)
        segment_midpoint = segment.midpoint

        # Get length
        new_segment = Segment(newp1, newp2)
        midpoint = new_segment.midpoint

        # TODO: Customizable precision
        self.text_item = TextSceneItem('{0:.2f}'.format(float(new_segment.length.evalf())))
        self.text_item.setTransform(self.text_item.sceneTransform().scale(1, -1))
        self.add_scene_item(self.text_item)

        bounding_rect = self.text_item.boundingRect()
        offset_x = 0
        offset_y = 0

        # Vertical Top
        if midpoint.y > segment_midpoint.y:
            offset_y = bounding_rect.height() / 2

        # Vertical Bottom
        if midpoint.y < segment_midpoint.y:
            offset_y = -bounding_rect.height() / 2

        self.text_item.setPos(midpoint.x + offset_x, midpoint.y + offset_y)

        # Point used to allow alligning dimension labels
        point_item = HiddenPointItem(midpoint)
        self.add_child_item(point_item)
