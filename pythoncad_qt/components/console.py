from PyQt4 import QtGui

from components.base import ComponentBase, VerticalLayout, HorizontalLayout


class ConsoleTitle(HorizontalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(ConsoleTitle, self).__init__(*args, **kwargs)
        self.title = QtGui.QLabel('Python Console')
        self.add_component(self.title)


class Console(VerticalLayout, ComponentBase):
    def __init__(self, drawing, *args, **kwargs):
        super(Console, self).__init__(*args, **kwargs)

        self.drawing = drawing

        self.title = ConsoleTitle(self)
        self.console = QtGui.QListWidget(self)
        # Test data, only for design
        self.console.addItem('Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win32')
        self.console.addItem('Type "help", "copyright", "credits" or "license" for more information.')
        self.console.addItem('>>>')

        self.add_component(self.title)
        self.add_component(self.console)
