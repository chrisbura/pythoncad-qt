from PyQt4 import QtGui, QtCore

from components.base import VerticalLayout, ComponentBase
from components.sidebar_panes.sidebar_pane import SidebarPane


class ConsolePaneWidget(VerticalLayout, ComponentBase):

    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(ConsolePaneWidget, self).__init__(*args, **kwargs)

        self.console = QtGui.QListWidget(self)
        # Test data, only for design
        self.console.addItem('Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win32')
        self.console.addItem('Type "help", "copyright", "credits" or "license" for more information.')
        self.console.addItem('>>>')

        self.add_component(self.console)


class ConsolePane(SidebarPane):

    def __init__(self, parent=None):
        super(ConsolePane, self).__init__(parent)

        self.stack = QtGui.QStackedWidget()
        self.add_component(self.stack)

    def add_document(self, document):
        console_view = ConsolePaneWidget()
        index = self.stack.addWidget(console_view)
        # TODO: Move to signal
        document.console_pane_index = index

    def switch_document(self, document):
        self.stack.setCurrentIndex(document.console_pane_index)
