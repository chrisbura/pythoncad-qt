#
# PythonCAD-Qt
# Copyright (C) 2015 Christopher Bura
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


class ItemManager(QtCore.QObject):

    add_scene_item = QtCore.pyqtSignal(object)
    remove_scene_item = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(ItemManager, self).__init__(*args, **kwargs)
        self.items = []

    def add_item(self, item):
        for child_item in item.traverse():
            for scene_item in child_item.scene_items:
                self.add_scene_item.emit(scene_item)

    def remove_item(self, item):
        for child_item in item.traverse():
            for scene_item in child_item.scene_items:
                self.remove_scene_item.emit(scene_item)
