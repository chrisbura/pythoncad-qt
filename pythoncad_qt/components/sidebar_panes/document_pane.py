from PyQt4 import QtGui, QtCore

from .sidebar_pane import SidebarPane
from ..buttons import PrimaryButton
from ..sidebar_widgets import FilterableTreeView


class DocumentPane(SidebarPane):

    document_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(DocumentPane, self).__init__(parent)

        # Mapping of QStandardItems to QStackWidget indexes
        # TODO: Must be a more 'qt' way to do this
        self.indexes = {}

        # Buttons
        self.new_document_button = PrimaryButton('Create new document')
        self.open_document_button = PrimaryButton('Open existing document')
        self.add_component(self.new_document_button)
        self.add_component(self.open_document_button)

        self.tree_widget = FilterableTreeView()
        self.add_component(self.tree_widget)

        # Root Elements
        self.open_document_root = QtGui.QStandardItem('Open Documents')
        self.open_document_root.setFlags(QtCore.Qt.NoItemFlags)
        self.tree_widget.model.appendRow(self.open_document_root)

        self.recent_document_root = QtGui.QStandardItem('Recent Documents')
        self.recent_document_root.setFlags(QtCore.Qt.NoItemFlags)
        self.tree_widget.model.appendRow(self.recent_document_root)

        # Add Tree Category Filters
        self.tree_widget.parent_select.addItem('Show All')
        self.tree_widget.parent_select.addItem('Open Documents')
        self.tree_widget.parent_select.addItem('Recent Documents')

        self.tree_widget.parent_select.currentIndexChanged.connect(
            self.parent_select_index_changed)

        # TODO: Implement 'Recent Items'
        recent_placeholder = QtGui.QStandardItem('None')
        recent_placeholder.setFlags(QtCore.Qt.NoItemFlags)
        self.recent_document_root.appendRow(recent_placeholder)

        # Start the two root elements in expanded state
        self.tree_widget.tree.expandAll()

        # Signals
        self.tree_widget.tree.clicked.connect(self.handle_click)
        self.tree_widget.tree.doubleClicked.connect(self.handle_double_click)

    def parent_select_index_changed(self, row):
        # TODO: Find more 'qt' way to do this, NoItemFlags prevents same model
        # from being used in QComboBox and QTreeView
        if row == 1:
            self.tree_widget.tree.setRootIndex(
                self.tree_widget.proxy_model.mapFromSource(
                    self.open_document_root.index()
                ))
        elif row == 2:
            self.tree_widget.tree.setRootIndex(
                self.tree_widget.proxy_model.mapFromSource(
                    self.recent_document_root.index()
                ))
        else:
            self.tree_widget.tree.setRootIndex(
                self.tree_widget.model.invisibleRootItem().index()
                )

    def add_document(self, document):
        item = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), document.title)
        self.indexes[item] = document.index

        # Signals
        document.title_changed.connect(item.setText)

        # Add item to model
        self.open_document_root.appendRow(item)

    def handle_click(self, index):
        """
        Used for switching between open documents
        """
        item = self.tree_widget.get_item_from_proxy_index(index)
        # If the item is a child of 'Open Documents' then switch the StackWidget
        # to that document
        if item.parent() is self.open_document_root:
            self.document_changed.emit(self.indexes[item])

    def handle_double_click(self, index):
        """
        Used for opening recent documents
        """
        item = self.tree_widget.get_item_from_proxy_index(index)
        # If the item is a child of 'Recent Documents' then open that document
        # on double click
        if item.parent() is self.recent_document_root:
            pass
