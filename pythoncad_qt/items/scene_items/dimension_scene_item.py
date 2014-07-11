
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
