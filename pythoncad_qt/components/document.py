from tempfile import NamedTemporaryFile

from PyQt4 import QtCore, QtGui

from pythoncad.drawing import Drawing

from components.base import ComponentBase, VerticalLayout, HorizontalLayout
from components.buttons import Button
from .console import Console


class DocumentStack(QtGui.QStackedWidget):
    pass


class DocumentView(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(DocumentView, self).__init__(*args, **kwargs)

        self.document_stack = DocumentStack()
        self.add_component(self.document_stack)

        # Open initial blank drawing on component creation
        self.open_document()

    def add_document(self, document):
        self.document_stack.addWidget(document)

    def open_document(self, filename=None):
        # TODO: check if document is open

        if filename is None:
            # Create blank drawing in temporary location
            # TODO: Use sqlite memory database instead of temp file
            temporary_file = NamedTemporaryFile(prefix='pycad_qt_', suffix='.pdr')
            filename = temporary_file.name
            temporary_file.close()

        # Open drawing
        drawing = Drawing(filename)
        document = DocumentWithConsole(drawing)

        # Add document to document stack
        self.add_document(document)


class ConsoleSplitter(QtGui.QSplitter):
    def __init__(self, *args, **kwargs):
        super(ConsoleSplitter, self).__init__(*args, **kwargs)
        self.setChildrenCollapsible(False)


class DocumentWithConsole(VerticalLayout, ComponentBase):
    def __init__(self, drawing, *args, **kwargs):
        super(DocumentWithConsole, self).__init__(*args, **kwargs)
        self.drawing = drawing
        self.setup_ui()

    def setup_ui(self):
        self.splitter = ConsoleSplitter(QtCore.Qt.Vertical)
        self.add_component(self.splitter)

        self.document = Document(self.drawing)
        self.console = Console(self.drawing)

        self.splitter.addWidget(self.document)
        self.splitter.addWidget(self.console)
        self.splitter.setStretchFactor(0, 9)
        self.splitter.setStretchFactor(1, 2)


class DocumentTitleLabel(QtGui.QLabel):
    pass


class TitleBar(HorizontalLayout, ComponentBase):

    layout_margins = QtCore.QMargins(0, 0, 11, 0)
    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.title = DocumentTitleLabel('Untitled')
        self.filename = QtGui.QLabel('filename.pdr')

        self.add_component(self.title)
        self.add_component(self.filename)
        self.add_component(Button('Save'))
        self.add_component(Button('Save As'))
        self.add_component(Button('Close'))

        self.add_stretch()

        self.expand = Button(QtGui.QIcon('images/maximize.png'), 'Expand')
        self.add_component(self.expand)

    def set_filename(self, filename):
        self.filename.setText(filename)


class Document(VerticalLayout, ComponentBase):
    def __init__(self, drawing, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

        self.drawing = drawing

        self.titlebar = TitleBar(self)
        self.titlebar.set_filename(self.drawing.db_path)

        self.graphicsview = QtGui.QGraphicsView(self)

        self.add_component(self.titlebar)
        self.add_component(self.graphicsview)
