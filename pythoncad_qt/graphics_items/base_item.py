
from PyQt4 import QtCore, QtGui

class BaseItem(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)
        self.children = []

    def add_child(self, item):
        item.parent = self
        self.children.append(item)
