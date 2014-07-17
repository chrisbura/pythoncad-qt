#
# PythonCAD-Qt
# Copyright (C) 2014 Christopher Bura
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from PyQt4 import QtGui, QtCore

from .sidebar_pane import SidebarPane
from ..buttons import PrimaryButton
from ..sidebar_widgets import FilterableTreeView


class DocumentPane(SidebarPane):

    document_changed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(DocumentPane, self).__init__(parent)

        # Buttons
        self.new_document_button = PrimaryButton('Create new document')
        self.open_document_button = PrimaryButton('Open existing document')
        self.add_component(self.new_document_button)
        self.add_component(self.open_document_button)

        self.tree_widget = FilterableTreeView()
        self.tree_widget.set_filter_placeholder('Filter Documents')
        self.add_component(self.tree_widget)

        # Root Elements
        self.open_document_root = QtGui.QStandardItem('Open Documents')
        self.open_document_root.setFlags(QtCore.Qt.NoItemFlags)
        self.open_document_root.setSelectable(False)
        self.tree_widget.model.appendRow(self.open_document_root)

        self.recent_document_root = QtGui.QStandardItem('Recent Documents')
        self.recent_document_root.setFlags(QtCore.Qt.NoItemFlags)
        self.recent_document_root.setSelectable(False)
        self.tree_widget.model.appendRow(self.recent_document_root)

        # TODO: Implement 'Recent Items'
        recent_placeholder = QtGui.QStandardItem('None')
        recent_placeholder.setFlags(QtCore.Qt.NoItemFlags)
        self.recent_document_root.appendRow(recent_placeholder)

        # Start the two root elements in expanded state
        self.tree_widget.tree.expandAll()

        # Signals
        self.tree_widget.tree.doubleClicked.connect(self.handle_double_click)

        selection_model = self.tree_widget.tree.selectionModel()
        selection_model.currentChanged.connect(self._activate_document)

    def add_document(self, document):
        item = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), document.title)
        item.setData(document, QtCore.Qt.UserRole)

        # Signals
        document.title_changed.connect(item.setText)

        # Add item to model
        self.open_document_root.appendRow(item)

        # Set new row active
        # TODO: Reselect active document after filtering
        # TODO: Do it on document_changed signal?
        selection_model = self.tree_widget.tree.selectionModel()
        selection_model.setCurrentIndex(
            self.tree_widget.proxy_model.mapFromSource(item.index()),
            QtGui.QItemSelectionModel.ClearAndSelect
        )

        self.document_changed.emit(document)

    def _activate_document(self, index):
        """
        Used for switching between open documents
        """
        item = self.tree_widget.get_item_from_proxy_index(index)
        # If the item is a child of 'Open Documents' then switch the StackWidget
        # to that document
        if item.parent() is self.open_document_root:
            document = index.data(QtCore.Qt.UserRole)
            self.document_changed.emit(document)

    def handle_double_click(self, index):
        """
        Used for opening recent documents
        """
        item = self.tree_widget.get_item_from_proxy_index(index)
        # If the item is a child of 'Recent Documents' then open that document
        # on double click
        if item.parent() is self.recent_document_root:
            pass
