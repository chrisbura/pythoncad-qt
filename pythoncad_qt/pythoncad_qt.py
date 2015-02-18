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

import sip
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore

import settings
from components.central_widget import CentralWidget
from components.sidebar import Sidebar
from components.buttons import PrimaryButton, DangerButton
from components.topbar import TopBar
from components.viewport import Viewport
from components.document import Document, DocumentView
from components.document_control import DocumentControl
from components.sidebar_panes import *
from dialogs.document_properties import DocumentPropertiesDialog
from input_filter import InputFilter
from item_manager import ItemManager
from command_manager import CommandManager
from graphics_items.snap_cursor import SnapCursor
from hover_event_manager import HoverEventManager

from models.drawing import Drawing
from models.layer import Layer

sip.setdestroyonexit(False)


class PythoncadQt(QtGui.QMainWindow):

    drawing_opened = QtCore.pyqtSignal(Drawing)

    def __init__(self):
        super(PythoncadQt, self).__init__()

        self.drawing = None
        self.viewport_expanded = False

        self.setWindowTitle('PythonCAD')

        with open(settings.STYLESHEET, 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # Central Widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 800)

        # Top Bar
        topbar = TopBar(self.central_widget)
        self.central_widget.add_component(topbar)

        # Content Widget
        content = Viewport(self.central_widget)
        self.central_widget.add_component(content)

        ### Splitter
        splitter = QtGui.QSplitter(content)
        self.splitter = splitter
        splitter.setChildrenCollapsible(True)
        content.layout.addWidget(splitter)

        ### Left Vertical Layout
        self.left_sidebar = Sidebar()

        # Command Pane
        self.command_pane = CommandPane()
        self.left_sidebar.add_pane('Commands', self.command_pane)

        # Document Viewport
        self.document_control = DocumentControl()
        scene = self.document_control.document.scene
        self.drawing_opened.connect(self.document_control.document.load_drawing)
        self.document_control.document.titlebar.expand_viewport.connect(self.toggle_expand)
        self.document_control.document.titlebar.open_properties.connect(self.open_properties)

        self.input_filter = InputFilter()
        self.command_manager = CommandManager()
        self.item_manager = ItemManager()

        # Input Filter
        self.command_manager.add_item.connect(self.input_filter.add_filters)
        scene.mouse_click.connect(self.input_filter.handle_click)
        scene.mouse_moved.connect(self.input_filter.handle_move)

        # Command Manager
        scene.escape_pressed.connect(self.command_manager.cancel_command)
        self.command_pane.command_started.connect(self.command_manager.start_command)
        self.input_filter.filtered_click.connect(self.command_manager.handle_click)
        self.input_filter.filtered_move.connect(self.command_manager.handle_move)

        # Item Manager
        self.command_manager.add_item.connect(self.item_manager.add_item)
        self.command_manager.remove_item.connect(self.item_manager.remove_item)
        self.item_manager.add_scene_item.connect(scene.addItem)
        self.item_manager.remove_scene_item.connect(scene.removeItem)
        scene.remove_item.connect(self.item_manager.remove_item)

        # Cursor
        self.cursor = SnapCursor(0, 0)
        self.cursor.hide()
        scene.addItem(self.cursor)

        self.input_filter.filtered_move.connect(self.cursor.set_position)
        self.command_manager.command_started.connect(self.cursor.show)
        self.command_manager.command_stopped.connect(self.cursor.hide)

        self.hover_manager = HoverEventManager()
        self.input_filter.filtered_move.connect(self.hover_manager.process_hover)

        # Right Sidebar
        self.right_sidebar = Sidebar()

        # Outline Pane
        outline_pane = OutlinePane()
        self.right_sidebar.add_pane('Outline', outline_pane)
        self.command_manager.add_item.connect(outline_pane.add_item)
        # TODO: Remove item on delete

        self.layer_pane = LayerPane()
        # console_pane = ConsolePane()

        self.right_sidebar.add_pane('Layers', self.layer_pane)
        # self.right_sidebar.add_pane('Console', console_pane)

        # Add Sidebars and document to central widget splitter
        splitter.addWidget(self.left_sidebar)
        splitter.addWidget(self.document_control)
        splitter.addWidget(self.right_sidebar)

        # Set initial splitter proportions
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 9)
        splitter.setStretchFactor(2, 2)

    def open_drawing(self):
        self.drawing = Drawing(title='New Drawing')

        self.drawing_opened.emit(self.drawing)
        self.drawing.layer_added.connect(self.layer_pane.layer_pane_widget.add_layer)
        self.layer_pane.layer_pane_widget.create_layer_button.clicked.connect(self.drawing.create_layer)
        self.drawing.title_changed.connect(self.document_control.document.titlebar.set_title)

        # Add default layer if drawing has no layers
        if self.drawing.layer_count == 0:
            self.drawing.add_layer(Layer(title='Default Layer'))

    def open_properties(self):
        document_properties_dialog = DocumentPropertiesDialog(
            drawing=self.drawing, parent=self)
        dialog_return = document_properties_dialog.exec_()

        if dialog_return == QtGui.QDialog.Accepted:
            # TODO: Error checking
            # TODO: Auto update title using signal
            drawing_title = str(document_properties_dialog.form.fields['title'].text())
            self.drawing.set_title(drawing_title)
        else:
            # TODO: Reset fields
            pass

    def toggle_expand(self):

        if self.left_sidebar.isVisible():
            self.left_sidebar.hide()
        else:
            self.left_sidebar.show()

        if self.right_sidebar.isVisible():
            self.right_sidebar.hide()
        else:
            self.right_sidebar.show()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setEffectEnabled(QtCore.Qt.UI_AnimateCombo, False)
    widget = PythoncadQt()
    # TODO: Allow opening documents via command line
    widget.open_drawing()
    widget.show()
    app.exec_()
