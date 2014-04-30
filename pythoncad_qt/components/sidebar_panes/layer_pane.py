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


class LayerPaneWidget(VerticalLayout, ComponentBase):

    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(LayerPaneWidget, self).__init__(*args, **kwargs)

        # Buttons
        self.manage_layer_button = PrimaryButton('Open layer Manager')
        self.create_layer_button = PrimaryButton('Create new layer')
        self.add_component(self.manage_layer_button)
        self.add_component(self.create_layer_button)

        # Model
        self.layer_model = QtGui.QStandardItemModel(self)

        # Tree
        self.layer_tree = LayerTreeView()
        self.layer_tree.setModel(self.layer_model)
        self.add_component(self.layer_tree)


class LayerPane(SidebarPane):
    def __init__(self, parent=None):
        super(LayerPane, self).__init__(parent)

        self.stack = QtGui.QStackedWidget()
        self.add_component(self.stack)

    def add_document(self, document):
        layer_view = LayerPaneWidget()
        index = self.stack.addWidget(layer_view)
        document.layer_pane_index = index

        root_item = layer_view.layer_model.invisibleRootItem()

        for layer in document.layers:
            item = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), layer.title)
            item.setData(layer, QtCore.Qt.UserRole)
            root_item.appendRow(item)

    def switch_document(self, document):
        self.stack.setCurrentIndex(document.layer_pane_index)

    def update(self, document):
        pass
