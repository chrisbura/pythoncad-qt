from PyQt4 import QtGui

from .base import VerticalLayout, ComponentBase


class Viewport(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(Viewport, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
