
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

        self.console_pane_widget = ConsolePaneWidget()
        self.add_component(self.console_pane_widget)
