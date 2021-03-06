#
# PythonCAD-Qt
# Copyright (C) 2014-2015 Christopher Bura
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

from components.buttons import PrimaryButton
from components.base import VerticalLayout, HorizontalLayout, ComponentBase


class CommandFilterProxy(QtGui.QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):

        index = self.sourceModel().index(source_row, 0, source_parent)

        if self.sourceModel().hasChildren(index):
            for child_index in range(index.model().rowCount(index)):
                if self.filterAcceptsRow(child_index, index):
                    return True
            return False

        return super(CommandFilterProxy, self).filterAcceptsRow(source_row, source_parent)


class ClearableLineEdit(QtGui.QLineEdit):
    def __init__(self, placeholder='', parent=None):
        super(ClearableLineEdit, self).__init__(parent)

        self.setPlaceholderText(placeholder)

        # Layout
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(0)
        # TODO: Find a way to do in stylesheets, QLayout can't be styled
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Clear Button
        self.clear_button = QtGui.QToolButton(self)
        self.clear_button.setCursor(QtCore.Qt.ArrowCursor)
        # TODO: Add clear on ESC
        self.clear_button.clicked.connect(self.clear_filter)

        self.layout.addWidget(self.clear_button, alignment=QtCore.Qt.AlignRight)

    def clear_filter(self):
        self.clear()


class CollapseExpandButtonBar(HorizontalLayout, ComponentBase):

    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(CollapseExpandButtonBar, self).__init__(*args, **kwargs)

        # Buttons
        self.collapse_button = PrimaryButton('Collapse All')
        self.expand_button = PrimaryButton('Expand All')

        self.add_component(self.collapse_button)
        self.add_component(self.expand_button)


# TODO: Doesn't work in PySide, even basic def paint... with super()
# SEE: https://bugreports.qt.io/browse/PYSIDE-152
class BoldParentDelegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not index.parent().isValid():
            # font-weight cannot currently be set via stylesheet
            # investigate in the future if things have changed
            option.font.setWeight(QtGui.QFont.Bold)
            option.palette.setColor(QtGui.QPalette.Text, QtGui.QColor('#566d7b'))
        super(BoldParentDelegate, self).paint(painter, option, index)


class FilterableTreeView(VerticalLayout, ComponentBase):
    layout_spacing = 6

    def __init__(self, model=QtGui.QStandardItemModel(), *args, **kwargs):
        super(FilterableTreeView, self).__init__(*args, **kwargs)

        self.model = model

        # Contents
        self.prepare_widgets()
        self.prepare_layout()

        # Signals
        self.filter.textChanged.connect(self.filter_tree)
        self.expand_collapse_bar.collapse_button.clicked.connect(self.tree.collapseAll)
        self.expand_collapse_bar.expand_button.clicked.connect(self.tree.expandAll)

    def prepare_widgets(self):
        # Filter (QLineEdit)
        self.filter = ClearableLineEdit(placeholder='Filter')

        # Setup Tree model and proxy model
        self.proxy_model = CommandFilterProxy(self)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)

        # Tree
        # TODO: Add collapse indicators
        self.tree = QtGui.QTreeView()
        self.tree.setRootIsDecorated(False)
        self.tree.setModel(self.proxy_model)
        self.tree.setIndentation(0)
        self.tree.setHeaderHidden(True)
        self.tree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # self.tree.setItemDelegate(BoldParentDelegate())
        self.tree.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tree.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # Button bar
        self.expand_collapse_bar = CollapseExpandButtonBar()

    def prepare_layout(self):
        # Add items to layout
        self.add_component(self.filter)
        self.add_component(self.tree)
        self.add_component(self.expand_collapse_bar)

    def set_filter_placeholder(self, text):
        self.filter.setPlaceholderText(text)

    def filter_tree(self):
        self.proxy_model.setFilterWildcard(self.filter.text())
        self.tree.expandAll()

    def get_item_from_proxy_index(self, index):
        return self.model.itemFromIndex(self.proxy_model.mapToSource(index))
