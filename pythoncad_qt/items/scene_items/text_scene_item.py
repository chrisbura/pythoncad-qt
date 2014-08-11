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


class TextSceneItem(QtGui.QGraphicsItem):

    # TODO: Settings
    padding = 5

    def __init__(self, text, *args, **kwargs):
        self.text = text

        super(TextSceneItem, self).__init__(*args, **kwargs)

        # TODO: Settings
        self.font = QtGui.QFont('Calibri', 12, QtGui.QFont.Bold)
        self.pen = QtGui.QPen(QtCore.Qt.gray)
        self.metrics = QtGui.QFontMetricsF(self.font)

    def boundingRect(self):
        rect = self.metrics.boundingRect(self.text)
        rect.adjust(-self.padding, -self.padding, self.padding, self.padding)
        rect.translate(-rect.center())
        return rect

    def paint(self, painter, option, *args, **kwargs):
        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.drawText(self.boundingRect(), QtCore.Qt.AlignCenter, self.text)
