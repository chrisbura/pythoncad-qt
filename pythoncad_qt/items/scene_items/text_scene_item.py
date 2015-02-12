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

import settings
from items.scene_items.scene_item import BasePen, ShapeDebugMixin, SceneItem


class PenMixin(object):
    """
    Used to add pen() and setPen() capabilities to
    custom items derived from QGraphicsItem
    """
    def __init__(self, *args, **kwargs):
        super(PenShim, self).__init__(*args, **kwargs)
        self._pen = QtGui.QPen()

    def setPen(self, pen):
        self.prepareGeometryChange()
        self._pen = pen
        self.update()

    def pen(self):
        return self._pen


class BaseTextGraphicsItem(PenMixin, QtGui.QGraphicsItem):
    # TODO(chrisbura): Add to settings
    padding = 5

    def __init__(self, text, *args, **kwargs):
        super(BaseTextGraphicsItem, self).__init__(*args, **kwargs)
        self.text = text
        # TODO(chrisbura): Add to settings
        self.font = QtGui.QFont('Calibri', 12, QtGui.QFont.Bold)
        self.metrics = QtGui.QFontMetricsF(self.font)

    def boundingRect(self):
        rect = self.metrics.boundingRect(self.text)
        rect.adjust(-self.padding, -self.padding, self.padding, self.padding)
        rect.translate(-rect.center())
        return rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        painter.setFont(self.font)
        painter.drawText(self.boundingRect(), QtCore.Qt.AlignCenter, self.text)


class TextSceneItem(SceneItem, BaseTextGraphicsItem):

    selected_colour = settings.SELECTED_COLOUR
    default_colour = QtCore.Qt.gray
    hover_colour = QtCore.Qt.blue
