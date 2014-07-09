
from PyQt4 import QtCore, QtGui

class BaseItem(QtCore.QObject):

    hover_enter = QtCore.pyqtSignal(object)
    hover_leave = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)
        self.children = []

    def add_child(self, item):
        item.parent = self
        self.children.append(item)
