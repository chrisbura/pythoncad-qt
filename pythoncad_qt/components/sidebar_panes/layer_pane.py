from PyQt4 import QtGui, QtCore

from ..buttons import PrimaryButton
from ..sidebar_widgets import FilterableTreeView
from .sidebar_pane import SidebarPane
from components.base import VerticalLayout, ComponentBase

# TODO: Set current selection to active_layer

class LayerTreeView(QtGui.QTreeView):
    def __init__(self, *args, **kwargs):
        super(LayerTreeView, self).__init__(*args, **kwargs)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)

class LayerPaneWidget(VerticalLayout, ComponentBase):

    layout_spacing = 6
    layer_changed = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(LayerPaneWidget, self).__init__(*args, **kwargs)

        # Buttons
        self.create_layer_button = PrimaryButton('Create new layer')
        self.add_component(self.create_layer_button)

        # Model
        self.layer_model = QtGui.QStandardItemModel(self)

        # Tree
        self.layer_tree = LayerTreeView()
        self.layer_tree.setModel(self.layer_model)
        self.add_component(self.layer_tree)

        # Signals
        self.layer_model.itemChanged.connect(self.update_layer)

        # Handle active layer selection
        selection_model = self.layer_tree.selectionModel()
        selection_model.currentChanged.connect(self._activate_layer)

    def add_layer(self, layer):
        # TODO: Cache for lots of layers
        layer_item = self._get_item(layer)
        root_item = self.layer_model.invisibleRootItem()
        root_item.appendRow(layer_item)

        selection_model = self.layer_tree.selectionModel()
        selection_model.setCurrentIndex(layer_item.index(),
            QtGui.QItemSelectionModel.ClearAndSelect
        )

        self.layer_changed.emit(layer)

    def add_layers(self, layers):
        for layer in layers:
            self.add_layer(layer)

    def _get_item(self, layer):
        item = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), layer.title)
        item.setCheckable(True)
        item.setCheckState(QtCore.Qt.Checked)
        item.setData(layer, QtCore.Qt.UserRole)
        return item

    def update_layer(self, item):
        # TODO: Must be a better way to do this
        layer = item.data(QtCore.Qt.UserRole)
        layer.set_title(item.text())

        # checkState can be 0, 1 (partially) or 2
        if item.checkState() == QtCore.Qt.Checked:
            layer.set_visibility(True)
        else:
            layer.set_visibility(False)

    def _activate_layer(self, index):
        item = self.layer_model.itemFromIndex(index)
        layer = index.data(QtCore.Qt.UserRole)
        self.layer_changed.emit(layer)


class LayerPane(SidebarPane):

    def __init__(self, parent=None):
        super(LayerPane, self).__init__(parent)

        self.stack = QtGui.QStackedWidget()
        self.add_component(self.stack)

    def add_document(self, document):
        layer_view = LayerPaneWidget()
        index = self.stack.addWidget(layer_view)
        document.layer_pane_index = index

        # Signals
        layer_view.layer_changed.connect(document.set_active_layer)
        layer_view.create_layer_button.clicked.connect(document.create_layer)
        document.layer_added.connect(layer_view.add_layer)

        layer_view.add_layers(document.layers)

    def switch_document(self, document):
        self.stack.setCurrentIndex(document.layer_pane_index)

    def update(self, document):
        pass
