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

from PyQt4 import QtCore, QtGui


# TODO: Have Items clean up scene items?
class Item(QtCore.QObject):

    name = 'Item'
    icon = 'images/commands/new.png'

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.parent = None
        self.child_items = []
        self.scene_items = []

    def add_scene_item(self, scene_item):
        scene_item.parent = self
        self.scene_items.append(scene_item)

    def add_child_item(self, child):
        child.parent = self
        self.child_items.append(child)

    def traverse(self):
        yield self
        for child in self.child_items:
            for item in child.traverse():
                yield item
