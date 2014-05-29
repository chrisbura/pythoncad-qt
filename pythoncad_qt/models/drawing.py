from PyQt4 import QtCore

from pythoncad.new_api import Drawing


class Drawing(Drawing, QtCore.QObject):
    # Pass around drawing object, allows connecting signals
    # So when title changes then everything that depends on title will also
    # change

    # TODO: Generalize to attribute change
    title_changed = QtCore.pyqtSignal(str)
    layer_added = QtCore.pyqtSignal(object)
    active_layer_changed = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(Drawing, self).__init__(*args, **kwargs)

        # Index position of drawing in QStackWidget
        self.index = None
        self.active_layer = None
        self.layer_pane_index = None
        self.console_pane_index = None

    def set_title(self, title):
        self.title = title
        self.title_changed.emit(self.title)

    def create_layer(self):
        layer = Layer(title='New Layer')
        self.add_layer(layer)

    def add_layer(self, layer):
        super(Drawing, self).add_layer(layer)
        self.layer_added.emit(layer)

    def add_entity(self, entity):
        self.active_layer.add_entity(entity)

    def set_active_layer(self, layer):
        self.active_layer = layer
        self.active_layer_changed.emit(layer)
