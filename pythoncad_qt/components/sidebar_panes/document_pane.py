from PyQt4 import QtGui

from .sidebar_pane import SidebarPane
from ..buttons import PrimaryButton
from ..sidebar_widgets import FilterableTreeView


class DocumentPane(SidebarPane):
    def __init__(self, parent=None):
        super(DocumentPane, self).__init__(parent)

        # Buttons
        self.new_document_button = PrimaryButton('Create new document')
        self.open_document_button = PrimaryButton('Open existing document')
        self.add_component(self.new_document_button)
        self.add_component(self.open_document_button)

        self.tree_widget = FilterableTreeView()
        self.add_component(self.tree_widget)

        self.setup_test_data()

    def setup_test_data(self):
        # Sample Data
        for item in ['Open Documents', 'Recent Documents']:
            root = QtGui.QStandardItem(item)
            root.setEditable(False)
            self.tree_widget.model.appendRow(root)

            for i in range(5):
                child = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), 'document{0}.pdr'.format(i+1))
                child.setEditable(False)
                root.appendRow(child)

        self.tree_widget.tree.expandAll()
