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

import math

from PyQt4 import QtCore, QtGui

import settings


class MoveEvent(object):
    def __init__(self, event, *args, **kwargs):
        super(MoveEvent, self).__init__(*args, **kwargs)
        self.raw_event = event
        self.x = self.raw_event.scenePos().x()
        self.y = self.raw_event.scenePos().y()


class DocumentScene(QtGui.QGraphicsScene):

    mouse_moved = QtCore.pyqtSignal(MoveEvent, list)
    mouse_click = QtCore.pyqtSignal(float, float, list)
    escape_pressed = QtCore.pyqtSignal()
    remove_item = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(DocumentScene, self).__init__(*args, **kwargs)

        # Arguments are x, y, width, height
        self.setSceneRect(-10000, -10000, 20000, 20000)

        # Grid
        self.setting_draw_grid = settings.DRAW_GRID
        self.grid_spacing = settings.GRID_SPACING

        # Axes
        self.setting_draw_axes = settings.DRAW_AXES

    def reset_scene(self):
        # TODO: Reset scene properly
        self.clear()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x, y = event.scenePos().x(), event.scenePos().y()
            self.mouse_click.emit(x, y, self.items(event.scenePos()))

        # Context menu to allow accurate selection of an item when multiple
        # items overlap
        if event.button() == QtCore.Qt.RightButton:
            # TODO: Display context menu with all items under scenePos
            # print('Right Mouse Button Clicked')
            pass

        super(DocumentScene, self).mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        # Cancel active command on esc
        # TODO: Handle focus, click command and bring focus to QGraphicsScene
        if event.key() == QtCore.Qt.Key_Escape:
            self.escape_pressed.emit()

        # Delete Selected Items
        # TODO: Decouple item
        selected_items = self.selectedItems()
        if event.key() == QtCore.Qt.Key_Delete and len(selected_items) > 0:
            for item in selected_items:
                self.remove_item.emit(item.parent)

        super(DocumentScene, self).keyReleaseEvent(event)

    def drawBackground(self, painter, rect):
        if self.setting_draw_grid:
            self.draw_grid(painter, rect)

        if self.setting_draw_axes:
            self.draw_axes(painter, rect)

    def toggle_grid(self):
        self.setting_draw_grid = not self.setting_draw_grid
        self.invalidate(self.sceneRect(), QtGui.QGraphicsScene.BackgroundLayer)

    def draw_grid(self, painter, rect):
        painter.save()

        # Grid Colours
        # TODO: Move to settings
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200, 100)))

        # Horizontal Grid
        top_count = -1 * int(math.floor(rect.top() / self.grid_spacing))
        bottom_count = int(math.ceil(rect.bottom() / self.grid_spacing))

        for i in range(bottom_count):
            y = i * self.grid_spacing
            painter.drawLine(rect.left(), y, rect.right(), y)

        for i in range(top_count):
            y = i * -self.grid_spacing
            painter.drawLine(rect.left(), y, rect.right(), y)

        # Vertical Grid
        left_count = -1 * int(math.floor(rect.left() / self.grid_spacing))
        right_count = int(math.ceil(rect.right() / self.grid_spacing))

        for i in range(left_count):
            x = i * -self.grid_spacing
            painter.drawLine(x, rect.top(), x, rect.bottom())

        for i in range(right_count):
            x = i * self.grid_spacing
            painter.drawLine(x, rect.top(), x, rect.bottom())

        painter.restore()

    def toggle_axes(self):
        self.setting_draw_axes = not self.setting_draw_axes
        self.invalidate(self.sceneRect(), QtGui.QGraphicsScene.BackgroundLayer)

    def draw_axes(self, painter, rect):
        painter.save()
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(rect.left(), 0, rect.right(), 0)
        painter.drawLine(0, rect.top(), 0, rect.bottom())
        painter.restore()

    def mouseMoveEvent(self, event):
        super(DocumentScene, self).mouseMoveEvent(event)
        items = self.items(event.scenePos())
        self.mouse_moved.emit(MoveEvent(event), items)
