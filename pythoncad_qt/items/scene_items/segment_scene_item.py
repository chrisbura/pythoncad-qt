
from PyQt4 import QtGui, QtCore

from items.scene_items import SceneItem


class SegmentSceneItem(SceneItem, QtGui.QGraphicsLineItem):
    def __init__(self, point1, point2):

        self.point1 = point1
        self.point2 = point2

        super(SegmentSceneItem, self).__init__(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y)

    def shape(self):
        p = QtGui.QPainterPath(QtCore.QPointF(self.point1.x, self.point1.y))
        p.lineTo(self.point2.x, self.point2.y)

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5.0)
        path = stroker.createStroke(p)

        return path
