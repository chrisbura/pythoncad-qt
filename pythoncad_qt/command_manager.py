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

from functools import partial

from PyQt4 import QtCore


class CommandManager(QtCore.QObject):

    coordinate_click = QtCore.pyqtSignal(float, float)
    mouse_move = QtCore.pyqtSignal(float, float)
    item_click = QtCore.pyqtSignal()
    add_item = QtCore.pyqtSignal(object)
    remove_item = QtCore.pyqtSignal(object)

    command_started = QtCore.pyqtSignal()
    command_stopped = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(CommandManager, self).__init__(*args, **kwargs)

        self.active_command = None

    def handle_click(self, x, y):
        self.coordinate_click.emit(x, y)

    def handle_move(self, x, y):
        self.mouse_move.emit(x, y)

    def start_command(self, command):
        if self.active_command:
            self.end_command()

        self.active_command = command()

        # Connect Signals to Command
        self.coordinate_click.connect(
            self.active_command.coordinate_received.emit)
        self.mouse_move.connect(self.active_command.mouse_received.emit)
        self.active_command.item_ready.connect(self.add_item.emit)
        self.active_command.item_remove.connect(self.remove_item.emit)
        self.active_command.command_finished.connect(self.end_command)

        self.active_command.start()
        self.command_started.emit()

        self.active_command.command_finished.connect(
            partial(self.start_command, command)
        )

    def end_command(self):
        self.coordinate_click.disconnect()
        self.mouse_move.disconnect()

        self.active_command = None

        self.command_stopped.emit()

    def cancel_command(self):
        if not self.active_command:
            return

        self.active_command.command_cancelled.emit()
        self.end_command()
