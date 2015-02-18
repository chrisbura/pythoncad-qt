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

from PyQt4 import QtGui, QtCore

import settings
from ..sidebar_widgets import FilterableTreeView
from .sidebar_pane import SidebarPane


class OutlinePane(SidebarPane):
    def __init__(self, parent=None):
        super(OutlinePane, self).__init__(parent)

        self.tree_widget = FilterableTreeView()
        self.tree_widget.tree.setIndentation(10)
        self.add_component(self.tree_widget)

    def add_item(self, item):
        model_item = QtGui.QStandardItem(QtGui.QIcon(item.icon), item.name)
        self.tree_widget.model.appendRow(model_item)
        self._get_children(item, model_item)

        self.tree_widget.tree.expandAll()

    def _get_children(self, item, model_item):
        if settings.DEBUG_OUTLINE_SCENEITEMS:
            for scene_item in item.scene_items:
                scene_item_row = QtGui.QStandardItem(str(scene_item.__class__.__name__))
                model_item.appendRow(scene_item_row)

        for child in item.child_items:
            child_item = QtGui.QStandardItem(QtGui.QIcon(child.icon), child.name)
            model_item.appendRow(child_item)
            self._get_children(child, child_item)
