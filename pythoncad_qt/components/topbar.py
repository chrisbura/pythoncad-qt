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

from .base import HorizontalLayout, ComponentBase
from .buttons import Button


class TopBar(HorizontalLayout, ComponentBase):
    layout_margins = QtCore.QMargins(0, 0, 11, 0)
    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(TopBar, self).__init__(*args, **kwargs)

        self.new_file_button = Button('New File')

        self.add_component(QtGui.QLabel('PythonCAD'))
        self.add_component(self.new_file_button)
        self.add_component(Button('Open File'))
        self.add_stretch()
        self.add_component(Button('Exit PythonCAD', clicked=QtGui.qApp.closeAllWindows))
