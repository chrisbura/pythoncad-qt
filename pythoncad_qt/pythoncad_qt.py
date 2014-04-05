import sip
from PyQt4 import QtGui, QtCore

from components.central_widget import CentralWidget
from components.sidebar import Sidebar
from components.buttons import PrimaryButton, DangerButton
from components.topbar import TopBar
from components.viewport import Viewport
from components.console import Console
from components.document import Document
from components.sidebar_panes import *

sip.setdestroyonexit(False)


class PythoncadQt(QtGui.QMainWindow):
    def __init__(self):
        super(PythoncadQt, self).__init__()

        self.setWindowTitle('PythonCAD')

        # TODO: Proper loading of resources
        stylesheet = open('stylesheets/pythoncad_qt.css', 'r')
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

        # Document Pane
        document_pane = DocumentPane()
        left_sidebar.add_pane('Documents', document_pane)

        # Outline Pane
        outline_pane = OutlinePane()
        left_sidebar.add_pane('Outline', outline_pane)

        # Layer Pane
        layer_pane = LayerPane()
        left_sidebar.add_pane('Layers', layer_pane)

        ### Center Vertical Layout
        center_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        center_splitter.setChildrenCollapsible(False)

        # Document
        document_widget = Document(center_splitter)

        # Console
        console_widget = Console(center_splitter)


        ### Right Vertical Layout
        properties_widget = Sidebar()

        properties_container = QtGui.QWidget()
        properties_container_layout = QtGui.QVBoxLayout(properties_container)
        # Note: Layout can't be styled via stylesheets
        properties_container_layout.setAlignment(QtCore.Qt.AlignTop)
        for i in range(3):
            group_box = QtGui.QGroupBox('Point {} Position'.format(i+1))
            group_box_layout = QtGui.QFormLayout(group_box)
            x_label = QtGui.QLabel('X')
            x_input = QtGui.QLineEdit()
            y_label = QtGui.QLabel('Y')
            y_input = QtGui.QLineEdit()
            group_box_layout.addRow(x_label, x_input)
            group_box_layout.addRow(y_label, y_input)
            properties_container_layout.addWidget(group_box)

        properties_container_layout.addWidget(PrimaryButton('Apply Changes'))
        properties_container_layout.addWidget(DangerButton('Reset'))

        properties_widget.add_pane('Properties', properties_container)

        splitter.addWidget(left_sidebar)
        splitter.addWidget(center_splitter)
        splitter.addWidget(properties_widget)

        # Set initial splitter proportions
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 9)
        splitter.setStretchFactor(2, 2)

        center_splitter.setStretchFactor(0, 9)
        center_splitter.setStretchFactor(1, 2)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setEffectEnabled(QtCore.Qt.UI_AnimateCombo, False)
    widget = PythoncadQt()
    widget.show()
    app.exec_()
