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

from functools import partial

from PyQt4 import QtCore, QtGui

from graphics_items.snap_cursor import SnapCursor


class InputManager(QtCore.QObject):

    mouse_click = QtCore.pyqtSignal(float, float, list)
    mouse_move = QtCore.pyqtSignal(float, float)
    command_finished = QtCore.pyqtSignal(object)
    add_item = QtCore.pyqtSignal(object)
    remove_item = QtCore.pyqtSignal(object)
    lock_input = QtCore.pyqtSignal(object)
    release_input = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(InputManager, self).__init__(*args, **kwargs)
        self.active_command = None
        self.horizontal_axis_locked = False
        self.horizontal_axis_value = None
        self.vertical_axis_locked = False
        self.vertical_axis_value = None

        # Add cursor to scene
        self.cursor = SnapCursor(0, 0)
        self.mouse_move.connect(self.cursor.set_position)
        self.cursor.hide()

    def lock_horizontal_axis(self, y):
        self.horizontal_axis_locked = True
        self.horizontal_axis_value = y

    def unlock_horizontal_axis(self):
        self.horizontal_axis_locked = False
        self.horizontal_axis_value = None

    def lock_vertical_axis(self, x):
        self.vertical_axis_locked = True
        self.vertical_axis_value = x

    def unlock_vertical_axis(self):
        self.vertical_axis_locked = False
        self.vertical_axis_value = None

    def lock_point(self, point):
        self.lock_horizontal_axis(point.y)
        self.lock_vertical_axis(point.x)

    def unlock_point(self):
        self.unlock_horizontal_axis()
        self.unlock_vertical_axis()

    def start_command(self, command):
        self.active_command = command()
        self.active_command.add_item.connect(self.add_item.emit)
        self.active_command.remove_item.connect(self.remove_item.emit)
        self.active_command.command_finished.connect(self.command_finished.emit)
        self.active_command.command_finished.connect(self.add_items)
        self.active_command.command_ended.connect(self.cancel_command)

        # Start command again after it finishes
        self.active_command.command_ended.connect(
            partial(self.start_command, command)
        )

        # These signals need to be disconnected
        self.mouse_click.connect(self.active_command.process_click)
        self.mouse_move.connect(self.active_command.process_move)
        self.lock_input.connect(self.active_command.snap_preview)
        self.release_input.connect(self.active_command.snap_release)

        # Show cursor
        if not self.cursor.scene():
            self.add_item.emit(self.cursor)
        self.cursor.show()

    def add_items(self, composite_items):
        for composite_item in composite_items:
            for item in composite_item.children:
                self.add_item.emit(item)
                item.parent.hover_enter.connect(self.lock_point)
                item.parent.hover_leave.connect(self.unlock_point)

    def cancel_command(self):
        if self.active_command:
            # TODO: Cleanup within command
            self.active_command.cleanup()
            self.mouse_click.disconnect(self.active_command.process_click)
            self.mouse_move.disconnect(self.active_command.process_move)
            self.lock_input.disconnect(self.active_command.snap_preview)
            self.release_input.disconnect(self.active_command.snap_release)
            self.active_command = None

            self.cursor.hide()

    def handle_click(self, x, y, items):

        if self.horizontal_axis_locked:
            y = self.horizontal_axis_value

        if self.vertical_axis_locked:
            x = self.vertical_axis_value

        self.mouse_click.emit(x, y, items)

    def handle_move(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()

        if self.horizontal_axis_locked:
            y = self.horizontal_axis_value

        if self.vertical_axis_locked:
            x = self.vertical_axis_value

        self.mouse_move.emit(x, y)
