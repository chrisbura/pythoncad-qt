from PyQt4 import QtCore

from pythoncad.new_api import Layer


class Layer(Layer, QtCore.QObject):

    title_changed = QtCore.pyqtSignal(str)
    visibility_changed = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Layer, self).__init__(*args, **kwargs)

    def set_title(self, title):
        self.title = title
        self.title_changed.emit(self.title)

    def set_visibility(self, visibility):
        self.visible = visibility
        self.visibility_changed.emit(self.visible)
