
from PyQt4 import QtGui

import settings
from items.scene_items.scene_item import BasePen


class ScenePreview(QtGui.QGraphicsItemGroup):
    def __init__(self, *args, **kwargs):
        super(ScenePreview, self).__init__(*args, **kwargs)

        self.pen = BasePen(settings.DEFAULT_COLOUR)

    def add_preview_item(self, item):
        item.setPen(self.pen)
        self.addToGroup(item)
