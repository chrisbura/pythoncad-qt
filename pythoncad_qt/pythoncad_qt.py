import sip
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

import settings
from components.central_widget import CentralWidget
from components.sidebar import Sidebar
from components.buttons import PrimaryButton, DangerButton
from components.topbar import TopBar
from components.viewport import Viewport
from components.document import Document, DocumentView
from components.document_control import DocumentControl
from components.sidebar_panes import *

from models.drawing import Drawing
from models.layer import Layer

sip.setdestroyonexit(False)


class PythoncadQt(QtGui.QMainWindow):

    drawing_opened = QtCore.pyqtSignal(Drawing)

    def __init__(self):
        super(PythoncadQt, self).__init__()

        self.drawing = None

        self.setWindowTitle('PythonCAD')

        with open(settings.STYLESHEET, 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # Central Widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 800)

        # Top Bar
        topbar = TopBar(self.central_widget)
        self.central_widget.add_component(topbar)

        # Content Widget
        content = Viewport(self.central_widget)
        self.central_widget.add_component(content)

        ### Splitter
        splitter = QtGui.QSplitter(content)
        splitter.setChildrenCollapsible(False)
        content.layout.addWidget(splitter)

        ### Left Vertical Layout
        left_sidebar = Sidebar()

        # Command Pane
        command_pane = CommandPane()
        left_sidebar.add_pane('Commands', command_pane)

        # Outline Pane
        # outline_pane = OutlinePane()
        # left_sidebar.add_pane('Outline', outline_pane)

        # Document Viewport
        document_control = DocumentControl()
        self.drawing_opened.connect(document_control.document.load_drawing)

        # Right Sidebar
        right_sidebar = Sidebar()

        self.layer_pane = LayerPane()
        console_pane = ConsolePane()

        right_sidebar.add_pane('Layers', self.layer_pane)
        right_sidebar.add_pane('Console', console_pane)

        # Add Sidebars and document to central widget splitter
        splitter.addWidget(left_sidebar)
        splitter.addWidget(document_control)
        splitter.addWidget(right_sidebar)

        # Set initial splitter proportions
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 9)
        splitter.setStretchFactor(2, 2)

        # command_pane.command_started.connect()

    def open_drawing(self):
        self.drawing = Drawing(title='New Drawing')

        self.drawing_opened.emit(self.drawing)
        self.drawing.layer_added.connect(self.layer_pane.layer_pane_widget.add_layer)
        self.layer_pane.layer_pane_widget.create_layer_button.clicked.connect(self.drawing.create_layer)

        # Add default layer if drawing has no layers
        if self.drawing.layer_count == 0:
            self.drawing.add_layer(Layer(title='Default Layer'))


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setEffectEnabled(QtCore.Qt.UI_AnimateCombo, False)
    widget = PythoncadQt()
    # TODO: Allow opening documents via command line
    widget.open_drawing()
    widget.show()
    app.exec_()
