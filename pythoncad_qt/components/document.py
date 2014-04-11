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

    def add_document(self, document):
        self.document_stack.addWidget(document)

    def open_document(self, filename=None):
        # TODO: check if document is open

        if filename is None:
            # Create blank drawing in temporary location
            temporary_file = NamedTemporaryFile(prefix='pycad_', suffix='.pdr')
            filename = temporary_file.name
            temporary_file.close()

        # Open drawing
        self.drawing = Drawing(filename)


class ConsoleSplitter(QtGui.QSplitter):
    def __init__(self, *args, **kwargs):
        super(ConsoleSplitter, self).__init__(*args, **kwargs)
        self.setChildrenCollapsible(False)


class DocumentWithConsole(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(DocumentWithConsole, self).__init__(*args, **kwargs)

        self.splitter = ConsoleSplitter(QtCore.Qt.Vertical)
        self.add_component(self.splitter)

        self.document = Document(self.splitter)
        self.console = Console(self.splitter)

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

class Document(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

        self.titlebar = TitleBar(self)
        self.graphicsview = QtGui.QGraphicsView(self)

        self.add_component(self.titlebar)
        self.add_component(self.graphicsview)
