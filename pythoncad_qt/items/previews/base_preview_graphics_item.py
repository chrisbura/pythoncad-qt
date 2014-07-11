
from PyQt4 import QtGui

import settings
from graphics_items.base_graphics_item import BasePen


class BasePreviewGraphicsItem(QtGui.QGraphicsItemGroup):
    def __init__(self, *args, **kwargs):
        super(BasePreviewGraphicsItem, self).__init__(*args, **kwargs)

        self.pen = BasePen(settings.DEFAULT_COLOUR)

    def add_preview_item(self, item):
        item.setPen(self.pen)
        self.addToGroup(item)
