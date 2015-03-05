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


class InputFilter(QtCore.QObject):

    filtered_click = QtCore.pyqtSignal(object, list, object)
    filtered_move = QtCore.pyqtSignal(object, list, object)

    def snap_coordinates(self, event, items):
        point = event.scenePos()

        for item in items:
            try:
                point = item.snap_coordinate(point)
            except AttributeError:
                pass

        return point

    def handle_click(self, event, items):
        point = self.snap_coordinates(event, items)
        self.filtered_click.emit(event, items, point)

    def handle_move(self, event, items):
        point = self.snap_coordinates(event, items)
        self.filtered_move.emit(event, items, point)
