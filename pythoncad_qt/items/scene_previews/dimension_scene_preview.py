
from PyQt4 import QtGui, QtCore

from sympy.geometry import Point, Line, Segment

from items.scene_previews import ScenePreview
from items.scene_items.scene_item import BasePen


# Override __contains__ to disable checking if point is on the line itself
# causes lag because update is called so many times
# TODO: Fix properly
class PreviewLine(Line):
    def __contains__(self, other):
        return False


# Override sympy.geometry.segment to return PreviewLine instead of Line
class PreviewSegment(Segment):
    def parallel_line(self, p):
        d = self.p1 - self.p2
        return PreviewLine(p, p + d)


class DimensionScenePreview(ScenePreview):
    def __init__(self, point1, point2, *args, **kwargs):
        super(DimensionScenePreview, self).__init__(*args, **kwargs)

        # TODO: Move to settings
        self.pen = BasePen(QtCore.Qt.gray)

        self.point1 = point1
        self.point2 = point2
        self.segment = PreviewSegment(point1, point2)
        self.lines = []

        for i in range(3):
            line = QtGui.QGraphicsLineItem()
            line.setPen(self.pen)
            self.lines.append(line)
            self.add_preview_item(line)

    def _get_point(self, segment, point):
        # Get perpendicular segment from the parallel line through point
        perpendicular_segment = segment.perpendicular_segment(point)

        try:
            # Convert tuple to list
            result = list(perpendicular_segment.points)
        except AttributeError:
            # perpendicular_segment returned a point (segment points are equal)
            return point

        # Remove original point
        result.remove(point)

        # Get new point
        return result.pop()

    def update(self, x, y):
        # Create a line parallel to the input coordinates at the
        # mouse coordinates
        parallel_line = self.segment.parallel_line(
            Point(x, y)
        )

        # First input point
        point1 = self._get_point(parallel_line, self.point1)
        self.lines[0].setLine(
            self.point1.x, self.point1.y,
            point1.x, point1.y
        )

        # Second input point
        point2 = self._get_point(parallel_line, self.point2)
        self.lines[1].setLine(
            self.point2.x, self.point2.y,
            point2.x, point2.y
        )

        # Join both points
        self.lines[2].setLine(
            point1.x, point1.y,
            point2.x, point2.y
        )
