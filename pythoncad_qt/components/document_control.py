from tempfile import NamedTemporaryFile
from functools import partial

from PyQt4 import QtCore, QtGui

from components.base import ComponentBase, VerticalLayout
from components.document import Document


# TODO: Find better place to put all the signal connections
class DocumentStack(QtGui.QStackedWidget):

    def process_command(self, command):
        current_widget = self.currentWidget()
        scene = current_widget.scene

        # Disconnect any currently connected slots
        try:
            self.disconnect_command(current_widget, command)
        except TypeError:
            # Exception is thrown if there are no currently connected slots
            pass

        scene.mouse_click.connect(command.process_click)
        scene.command_cancelled.connect(command.cancel)
        scene.mouse_move.connect(command.process_move)
        scene.lock_input.connect(command.snap_preview)
        scene.release_input.connect(command.snap_release)
        # Removes all scene connected slots, must be last to prevent removing
        # ones that are still required
        scene.command_cancelled.connect(
            partial(self.disconnect_command, current_widget, command)
        )

        command.command_finished.connect(scene.add_composite_item)
        command.add_item.connect(scene.addItem)
        command.remove_item.connect(scene.removeItem)
        command.command_ended.connect(
            partial(self.disconnect_command, current_widget, command)
        )

    def disconnect_command(self, current, command):
        current.scene.mouse_click.disconnect()
        current.scene.command_cancelled.disconnect()
        # Don't disconnect all mouse_move slots, still needed for things like
        # coordinate display
        current.scene.mouse_move.disconnect(command.process_move)


class DocumentControl(VerticalLayout, ComponentBase):

    def __init__(self, *args, **kwargs):
        super(DocumentControl, self).__init__(*args, **kwargs)

        self.document = Document()
        self.add_component(self.document)
