
from PyQt4 import QtCore, QtGui

class Item(QtCore.QObject):

    hover_enter = QtCore.pyqtSignal(object)
    hover_leave = QtCore.pyqtSignal()
    lock_horizontal = QtCore.pyqtSignal(float)
    lock_vertical = QtCore.pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.children = []

    def add_child(self, item):
        item.parent = self
        self.children.append(item)