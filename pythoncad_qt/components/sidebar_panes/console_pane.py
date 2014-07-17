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

from PyQt4 import QtGui, QtCore

from components.base import VerticalLayout, ComponentBase
from components.sidebar_panes.sidebar_pane import SidebarPane


class ConsolePaneWidget(VerticalLayout, ComponentBase):

    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(ConsolePaneWidget, self).__init__(*args, **kwargs)

        self.console = QtGui.QListWidget(self)
        # Test data, only for design
        self.console.addItem('Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win32')
        self.console.addItem('Type "help", "copyright", "credits" or "license" for more information.')
        self.console.addItem('>>>')

        self.add_component(self.console)


class ConsolePane(SidebarPane):
    def __init__(self, parent=None):
        super(ConsolePane, self).__init__(parent)

        self.console_pane_widget = ConsolePaneWidget()
        self.add_component(self.console_pane_widget)
