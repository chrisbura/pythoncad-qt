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


# TODO: Have Items clean up scene items?
class Item(QtCore.QObject):

    name = 'Item'
    icon = 'images/commands/new.png'

    hover_enter = QtCore.pyqtSignal(object)
    hover_leave = QtCore.pyqtSignal()
    deleted = QtCore.pyqtSignal()
    remove_scene_item = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.parent = None
        self.child_items = []
        self.scene_items = []

        self.input_filters = []

        self.delete.connect(self.delete_item)

    def add_scene_item(self, scene_item):
        scene_item.parent = self
        self.scene_items.append(scene_item)

    def add_child_item(self, child):
        child.parent = self
        self.child_items.append(child)

    def get_scene_items(self):
        for scene_item in self.scene_items:
            yield scene_item
        for child in self.child_items:
            for item in child.get_scene_items():
                yield item

    def delete_item(self):
        for scene_item in self.get_scene_items():
            self.remove_scene_item.emit(scene_item)

    def traverse(self):
        yield self
        for child in self.child_items:
            for item in child.traverse():
                yield item

    def filters(self):
        return self.input_filters

    def add_filter(self, input_filter):
        self.input_filters.append(input_filter)

    def activate_filters(self, *args):
        for input_filter in self.input_filters:
            input_filter.set_active(True)

    def deactivate_filters(self, *args):
        for input_filter in self.input_filters:
            input_filter.set_active(False)
