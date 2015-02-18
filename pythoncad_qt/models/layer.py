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

from pythoncad.new_api import Layer


class Layer(Layer, QtCore.QObject):

    title_changed = QtCore.pyqtSignal(str)
    visibility_changed = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Layer, self).__init__(*args, **kwargs)

    def set_title(self, title):
        self.title = title
        self.title_changed.emit(self.title)

    def set_visibility(self, visibility):
        self.visible = visibility
        self.visibility_changed.emit(self.visible)
