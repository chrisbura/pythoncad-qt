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

from functools import partial

from PyQt4 import QtCore


class Command(QtCore.QObject):

    click_received = QtCore.pyqtSignal(object, list, object)
    mouse_received = QtCore.pyqtSignal(float, float)
    command_finished = QtCore.pyqtSignal()
    command_cancelled = QtCore.pyqtSignal()

    item_ready = QtCore.pyqtSignal(object)
    item_remove = QtCore.pyqtSignal(object)
    preview_ready = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self._inputs = []
        self.active_input = None
        self.remaining_inputs = None

    def inputs(self):
        return self._inputs

    def add_input(self, input_):
        self._inputs.append(input_)

    def start(self):
        self.remaining_inputs = iter(self._inputs)
        self.next_input()

    def next_input(self):
        # Get next input
        try:
            self.active_input = self.remaining_inputs.next()
        except StopIteration:
            self.command_finished.emit()
            return

        # Connect *_received signals to next input
        self.click_received.connect(self.active_input.handle_click)
        self.mouse_received.connect(self.active_input.handle_move)

        # When an input is valid, disconnect it from the *_received signals
        self.active_input.input_valid.connect(
            partial(self.click_received.disconnect, self.active_input.handle_click))
        self.active_input.input_valid.connect(
            partial(self.mouse_received.disconnect, self.active_input.handle_move))

        # On valid input continue to the next input
        self.active_input.input_valid.connect(self.next_input)
