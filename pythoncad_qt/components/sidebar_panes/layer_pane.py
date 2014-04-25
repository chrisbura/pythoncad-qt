from PyQt4 import QtGui

from ..buttons import PrimaryButton
from ..sidebar_widgets import FilterableTreeView
from .sidebar_pane import SidebarPane


class LayerPane(SidebarPane):
    def __init__(self, parent=None):
        super(LayerPane, self).__init__(parent)

        # Buttons
        self.manage_layer_button = PrimaryButton('Open layer Manager')
        self.add_component(self.manage_layer_button)
        self.create_layer_button = PrimaryButton('Create new layer')
        self.add_component(self.create_layer_button)

        self.tree_widget = FilterableTreeView()
        self.add_component(self.tree_widget)

        self.setup_test_data()

    def setup_test_data(self):
        # Sample Data
        root_item = self.tree_widget.model.invisibleRootItem()
        for i in range(5):
            row = QtGui.QStandardItem('Layer {}'.format(i+1))
            root_item.appendRow(row)
