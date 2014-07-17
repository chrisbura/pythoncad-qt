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


class SnapCursor(QtGui.QGraphicsRectItem):
    def __init__(self, x, y):

        self.width = 10
        self.x, self.y = x, y

        super(SnapCursor, self).__init__(self.get_rect(x, y))

        self.pen = QtGui.QPen()
        self.pen.setColor(QtCore.Qt.magenta)
        self.pen.setWidth(2)
        self.setPen(self.pen)

    def set_position(self, x, y):
        self.setRect(self.get_rect(x, y))

    def get_rect(self, x, y):
        return QtCore.QRectF(
            x - self.width / 2,
            y - self.width / 2,
            self.width,
            self.width
        )
