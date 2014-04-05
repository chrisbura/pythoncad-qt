from PyQt4 import QtCore, QtGui

from .base import HorizontalLayout, ComponentBase
from .buttons import Button


class TopBar(HorizontalLayout, ComponentBase):
    layout_margins = QtCore.QMargins(0, 0, 11, 0)
    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(TopBar, self).__init__(*args, **kwargs)

        self.add_component(QtGui.QLabel('PythonCAD'))
        self.add_component(Button('New File'))
        self.add_component(Button('Open File'))
        self.add_stretch()
        self.add_component(Button('Exit PythonCAD'))
