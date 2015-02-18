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

from .base import VerticalLayout, ComponentBase


class SidebarPaneSelector(QtGui.QComboBox):
    def __init__(self, *args, **kwargs):
        super(SidebarPaneSelector, self).__init__(*args, **kwargs)

        self.item_delegate = QtGui.QStyledItemDelegate()
        self.setItemDelegate(self.item_delegate)


class SidebarPaneStack(QtGui.QStackedWidget):
    pass


class Sidebar(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(Sidebar, self).__init__(*args, **kwargs)

        self.pane_selector = SidebarPaneSelector()
        self.add_component(self.pane_selector)

        self.pane_stack = SidebarPaneStack()
        self.add_component(self.pane_stack)

        self.pane_selector.currentIndexChanged.connect(
            self.pane_stack.setCurrentIndex
        )

    def add_pane(self, title, pane):
        # TODO: Error checking
        self.pane_selector.addItem(title)
        self.pane_stack.addWidget(pane)
