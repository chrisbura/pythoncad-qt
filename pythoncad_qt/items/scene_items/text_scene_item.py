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
from items.scene_items.scene_item import BasePen, ShapeDebugMixin


class BaseTextGraphicsItem(QtGui.QGraphicsItem):
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
        painter.setFont(self.font)
        painter.drawText(self.boundingRect(), QtCore.Qt.AlignCenter, self.text)


class TextSceneItem(ShapeDebugMixin, BaseTextGraphicsItem):

    selected_colour = settings.SELECTED_COLOUR
    default_colour = QtCore.Qt.gray
    hover_colour = QtCore.Qt.blue

    def __init__(self, *args, **kwargs):
        super(TextSceneItem, self).__init__(*args, **kwargs)

        # TODO: Settings
        self.pen = QtGui.QPen(QtCore.Qt.gray)
        self.hover_pen = QtGui.QPen(QtCore.Qt.blue)
        self.selected_pen = BasePen(self.selected_colour)

        self.hover = False

        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        # if option.state & QtGui.QStyle.State_MouseOver:
            # painter.setPen(self.hover_pen)

        if self.hover:
            painter.setPen(self.hover_pen)

        if option.state & QtGui.QStyle.State_Selected:
            painter.setPen(self.selected_pen)

        super(TextSceneItem, self).paint(painter, option, widget)

    def hoverEnterEvent(self, event):
        self.hover = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hover = False
        self.update()
