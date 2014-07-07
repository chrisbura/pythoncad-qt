
from PyQt4 import QtGui

from graphics_items.base_preview_graphics_item import BasePreviewGraphicsItem
from graphics_items.point_graphics_item import PointGraphicsItem


class SegmentPreviewGraphicsItem(BasePreviewGraphicsItem):
    def __init__(self, point, *args, **kwargs):
        super(SegmentPreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.point = point

        # Starting Point
        self.starting_point = PointGraphicsItem(self.point)
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

    def update(self, event):
        self.segment.setLine(
            self.point.x, self.point.y,
            event.scenePos().x(), event.scenePos().y()
        )
