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
