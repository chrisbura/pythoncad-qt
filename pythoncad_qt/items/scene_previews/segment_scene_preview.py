
from PyQt4 import QtGui

from items.scene_previews import ScenePreview
from items.scene_items import PointSceneItem


class SegmentScenePreview(ScenePreview):
    def __init__(self, point, *args, **kwargs):
        super(SegmentScenePreview, self).__init__(*args, **kwargs)

        self.point = point

        # Starting Point
        self.starting_point = PointSceneItem(self.point)
        self.add_preview_item(self.starting_point)

        # Segment
        # Uses regular QGraphicsLineItem because shape() override on
        # SegmentGraphicsItem takes a lot of processing
        # TODO: Extract shape to be only on display item, want line thickness
        self.segment = QtGui.QGraphicsLineItem(
            self.point.x, self.point.y,
            self.point.x, self.point.y
        )
        self.add_preview_item(self.segment)

    def update(self, x, y):
        self.segment.setLine(
            self.point.x, self.point.y,
            x, y
        )
