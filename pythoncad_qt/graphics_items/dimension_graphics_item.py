from sympy.geometry import Point, Segment

from PyQt4 import QtGui, QtCore

from graphics_items.base_item import BaseItem
from graphics_items.segment_graphics_item import SegmentGraphicsItem
from graphics_items.point_graphics_item import PointGraphicsItem


class DimensionItem(BaseItem):
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

        # TODO: Use path instead of discreet items, or highlight all items

        self.segment = DimensionGraphicsItem(
            perpendicular_line_p1_points[0],
            perpendicular_line_p2_points[0]
        )
        self.add_child(self.segment)

        self.segment_p1 = DimensionGraphicsItem(
            point1,
            perpendicular_line_p1_points[0]
        )
        self.add_child(self.segment_p1)

        self.segment_p2 = DimensionGraphicsItem(
            point2,
            perpendicular_line_p2_points[0]
        )
        self.add_child(self.segment_p2)

        self.text = QtGui.QGraphicsSimpleTextItem('{0}'.format(segment.length))
        self.text.setPos(point3.x, point3.y)
        # TODO: DocumentView.scale causes text to be flipped, need to get
        # proper mapping from scene
        self.text.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True)
        self.add_child(self.text)


class DimensionGraphicsItem(SegmentGraphicsItem):
    default_colour = QtCore.Qt.gray
    hover_colour = QtCore.Qt.blue
