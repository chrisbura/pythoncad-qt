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

from PyQt4 import QtCore, QtGui

class Item(QtCore.QObject):

    hover_enter = QtCore.pyqtSignal(object)
    hover_leave = QtCore.pyqtSignal()
    lock_horizontal = QtCore.pyqtSignal(float)
    unlock_horizontal = QtCore.pyqtSignal()
    lock_vertical = QtCore.pyqtSignal(float)
    unlock_vertical = QtCore.pyqtSignal()
    deleted = QtCore.pyqtSignal()
    remove_scene_item = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.children = []
        self.items = []

    # TODO: Move to scene_items instead of children
    def add_child(self, item):
        item.parent = self
        self.children.append(item)

    def add_item(self, item):
        item.parent = self
        self.deleted.connect(item.delete)
        self.items.append(item)

    def delete(self):
        # TODO: Yield instead of signals?
        # TODO: Merge with get_items
        for item in self.children:
            self.remove_scene_item.emit(item)
        self.deleted.emit()

    # TODO: Audit/Refactor
    def get_items(self):
        for item in self.items:
            for scene_item in item.children:
                yield scene_item
            for item_ in item.get_items():
                yield item_
