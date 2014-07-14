
from functools import partial

from PyQt4 import QtCore, QtGui


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

    def start_command(self, command):
        self.active_command = command()
        self.active_command.add_item.connect(self.add_item.emit)
        self.active_command.remove_item.connect(self.remove_item.emit)
        self.active_command.command_finished.connect(self.command_finished.emit)
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

    def cancel_command(self):
        if self.active_command:
            # TODO: Cleanup within command
            self.active_command.cleanup()
            self.mouse_click.disconnect(self.active_command.process_click)
            self.mouse_move.disconnect(self.active_command.process_move)
            self.lock_input.disconnect(self.active_command.snap_preview)
            self.release_input.disconnect(self.active_command.snap_release)
            self.active_command = None

    def handle_click(self, x, y, items):
        self.mouse_click.emit(x, y, items)

    def handle_move(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        self.mouse_move.emit(x, y)
