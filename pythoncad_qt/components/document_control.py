from tempfile import NamedTemporaryFile
from functools import partial

from PyQt4 import QtCore, QtGui

from models.drawing import Drawing
from models.layer import Layer
from components.base import ComponentBase, VerticalLayout
from components.document import Document


# TODO: Find better place to put all the signal connections
class DocumentStack(QtGui.QStackedWidget):

    def process_command(self, command):
        current_widget = self.currentWidget()

        # Disconnect any currently connected slots
        try:
            self.disconnect_command(current_widget)
        except TypeError:
            # Exception is thrown if there are no currently connected slots
            pass

        current_widget.scene.active_command_click.connect(command.process_click)
        current_widget.scene.command_cancelled.connect(command.cancel)
        current_widget.scene.mouse_move.connect(command.process_move)
        # Removes all scene connected slots, must be last to prevent removing
        # ones that are still required
        current_widget.scene.command_cancelled.connect(
            partial(self.disconnect_command, current_widget)
        )

        command.add_preview.connect(current_widget.scene.addItem)
        command.remove_preview.connect(current_widget.scene.removeItem)
        command.add_item.connect(current_widget.scene.addItem)
        command.command_ended.connect(
            partial(self.disconnect_command, current_widget)
        )

    def disconnect_command(self, current):
        current.scene.active_command_click.disconnect()
        current.scene.command_cancelled.disconnect()
        current.scene.mouse_move.disconnect()


class DocumentControl(VerticalLayout, ComponentBase):

    # TODO: Move to Drawing.__init__
    document_opened = QtCore.pyqtSignal(object)
    command_cancelled = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(DocumentControl, self).__init__(*args, **kwargs)

        self.document_stack = DocumentStack()
        self.add_component(self.document_stack)

    def add_document(self, document):
        """
        Adds document widget to DocumentStack
        returns index position of new widget
        """
        return self.document_stack.addWidget(document)

    def switch_document(self, document):
        self.document_stack.setCurrentIndex(document.index)

    def open_document(self, filename=None):
        # TODO: check if document is open

        if filename is None:
            # Create blank drawing in temporary location
            # TODO: Use sqlite memory database instead of temp file
            # temporary_file = NamedTemporaryFile(prefix='pycad_qt_', suffix='.pdr')
            # filename = temporary_file.name
            # temporary_file.close()
            pass

        # Open drawing
        drawing = Drawing(title='New Drawing {0}'.format(self.document_stack.count() + 1))
        document = Document(drawing)

        # Add default layer if drawing has no layers
        if drawing.layer_count == 0:
            drawing.add_layer(Layer(title='Default Layer'))

        # Add document to document stack
        index = self.add_document(document)
        drawing.index = index

        # Activate new/opened document
        self.document_stack.setCurrentIndex(index)

        self.document_opened.emit(drawing)

        document.scene.command_cancelled.connect(self._command_cancelled)
        # document.scene.entity_added.connect(drawing.add_entity)

    def _command_cancelled(self):
        self.command_cancelled.emit()
