from tempfile import NamedTemporaryFile

from PyQt4 import QtCore, QtGui

from pythoncad.new_api import Drawing, Point, Layer

from components.base import ComponentBase, VerticalLayout, HorizontalLayout
from components.buttons import Button
from dialogs.document_properties import DocumentPropertiesDialog
from commands.inputs import PointInput
from graphics_items.point_graphics_item import PointGraphicsItem

# TODO: Split up file


class Drawing(Drawing, QtCore.QObject):
    # Pass around drawing object, allows connecting signals
    # So when title changes then everything that depends on title will also
    # change

    # TODO: Generalize to attribute change
    title_changed = QtCore.pyqtSignal(str)
    layer_added = QtCore.pyqtSignal(object)
    active_layer_changed = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(Drawing, self).__init__(*args, **kwargs)

        # Index position of drawing in QStackWidget
        self.index = None
        self.active_layer = None
        self.layer_pane_index = None
        self.console_pane_index = None

    def set_title(self, title):
        self.title = title
        self.title_changed.emit(self.title)

    def create_layer(self):
        layer = Layer(title='New Layer')
        self.add_layer(layer)

    def add_layer(self, layer):
        super(Drawing, self).add_layer(layer)
        self.layer_added.emit(layer)

    def add_entity(self, entity):
        self.active_layer.add_entity(entity)

    def set_active_layer(self, layer):
        self.active_layer = layer
        self.active_layer_changed.emit(layer)


class Layer(Layer, QtCore.QObject):

    title_changed = QtCore.pyqtSignal(str)
    visibility_changed = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Layer, self).__init__(*args, **kwargs)

    def set_title(self, title):
        self.title = title
        self.title_changed.emit(self.title)

    def set_visibility(self, visibility):
        self.visible = visibility
        self.visibility_changed.emit(self.visible)


class DocumentStack(QtGui.QStackedWidget):
    def process_command(self, command):
        current_widget = self.currentWidget()
        # TODO: Decouple with signals
        current_widget.document.scene.active_command = command()


class DocumentView(VerticalLayout, ComponentBase):

    # TODO: Move to Drawing.__init__
    document_opened = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(DocumentView, self).__init__(*args, **kwargs)

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

        # document.scene.entity_added.connect(drawing.add_entity)


class DocumentTitleLabel(QtGui.QLabel):
    pass


class TitleBar(HorizontalLayout, ComponentBase):

    layout_margins = QtCore.QMargins(0, 0, 11, 0)
    layout_spacing = 6

    def __init__(self, drawing, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.drawing = drawing

        # TODO: Double click to edit title
        self.title = DocumentTitleLabel(self.drawing.title)
        self.filename = QtGui.QLabel()

        self.add_component(self.title)
        self.add_component(self.filename)
        self.add_component(Button('Save'))
        self.add_component(Button('Save As'))
        self.add_component(Button('Properties',
            clicked=self.open_document_properties_dialog))
        self.add_component(Button('Close'))

        self.add_stretch()

        self.expand = Button(QtGui.QIcon('images/maximize.png'), 'Expand')
        self.add_component(self.expand)

    def set_filename(self, filename):
        self.filename.setText(filename)

    def set_title(self, title):
        self.title.setText(title)

    def open_document_properties_dialog(self):
        document_properties_dialog = DocumentPropertiesDialog(
            drawing=self.drawing, parent=self)
        dialog_return = document_properties_dialog.exec_()

        if dialog_return == QtGui.QDialog.Accepted:
            # TODO: Error checking
            # TODO: Auto update title using signal
            drawing_title = str(document_properties_dialog.form.fields['title'].text())
            self.drawing.set_title(drawing_title)
            self.set_title(drawing_title)
        else:
            # TODO: Reset fields
            print 'Rejected'


class DocumentScene(QtGui.QGraphicsScene):

    active_command_click = QtCore.pyqtSignal(object)
    entity_added = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(DocumentScene, self).__init__(*args, **kwargs)

        # Arguments are x, y, width, height
        self.setSceneRect(-10000, -10000, 20000, 20000)

        # Commands
        self.active_command = None

        self.active_command_click.connect(self.handle_click)

    def mouseReleaseEvent(self, event):
        # Split mouseReleaseEvent using signals to prevent large method
        if event.button() == QtCore.Qt.LeftButton and self.active_command is not None:
            self.active_command_click.emit(event)

        super(DocumentScene, self).mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        # Cancel active command on esc
        # TODO: Handle focus, click command and bring focus to QGraphicsScene
        if event.key() == QtCore.Qt.Key_Escape and self.active_command is not None:
            # TODO: Emit command canceled signal
            # TODO: deselect command on cancel
            self.active_command = None
            print 'Cancel'

    def handle_click(self, event):
        command = self.active_command
        current_input = command.inputs[command.active_input]

        if isinstance(current_input, PointInput):
            current_input.value = Point(
                event.scenePos().x(),
                event.scenePos().y())

        command.active_input = command.active_input + 1

        if command.active_input == len(command.inputs):
            # Get QGraphics*Item
            graphics_item = command.apply_command()
            self.entity_added.emit(graphics_item.entity)
            self.addItem(graphics_item)
            self.active_command = None

class SceneCoordinates(QtGui.QLabel):
    pass


class GraphicsStatusBar(HorizontalLayout, ComponentBase):
    layout_margins = QtCore.QMargins(5, 5, 5, 5)

    def __init__(self, *args, **kwargs):
        super(GraphicsStatusBar, self).__init__(*args, **kwargs)

        self.add_stretch()
        self.scene_coordinates = SceneCoordinates('X: 0.000 Y: 0.000')
        self.add_component(self.scene_coordinates)


class Document(VerticalLayout, ComponentBase):
    def __init__(self, drawing, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

        self.drawing = drawing

        # TODO: Find better way to pass around drawing
        self.titlebar = TitleBar(drawing=self.drawing)
        self.titlebar.set_filename('')
        self.titlebar.set_title('{title}'.format(title=self.drawing.title))

        self.scene = DocumentScene(parent=self)
        self.view = QtGui.QGraphicsView(self.scene, parent=self)
        # Flip Y axis
        self.view.scale(1, -1)

        self.status_bar = GraphicsStatusBar()

        self.add_component(self.titlebar)
        self.add_component(self.view)
        self.add_component(self.status_bar)
