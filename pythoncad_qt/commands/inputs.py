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

from PyQt4 import QtCore

from items.scene_items.point_scene_item import PointSceneItem


class Input(QtCore.QObject):

    input_valid = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)

    def handle_click(self, event, items, point):
        self.input_valid.emit()

    def handle_item(self):
        # TODO: Hookup item handling
        # TODO(chrisbura): Have filter class pass through only required item types to command
        self.input_valid.emit()

    def handle_move(self, x, y):
        pass


class CoordinateInput(Input):
    def __init__(self, *args, **kwargs):
        super(CoordinateInput, self).__init__(*args, **kwargs)
        self.x = None
        self.y = None

    def handle_click(self, event, items, point):
        self.x, self.y = point.x(), point.y()
        self.input_valid.emit()


class ItemInput(Input):
    pass


class PointInput(Input):
    def __init__(self, *args, **kwargs):
        super(PointInput, self).__init__(*args, **kwargs)
        self.point = None
        self.x = None
        self.y = None

    def handle_click(self, event, items, point):
        self.point = next((item for item in items if isinstance(item, PointSceneItem)), None)

        if self.point:
            self.x = self.point.scenePos().x()
            self.y = self.point.scenePos().y()
            self.input_valid.emit()


class SegmentInput(ItemInput):
    pass
