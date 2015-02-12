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

from functools import partial

from PyQt4 import QtGui, QtCore

from .sidebar_pane import SidebarPane
from ..sidebar_widgets import FilterableTreeView

# Commands
from commands.point_command import PointCommand
from commands.segment_command import SegmentCommand
from commands.circle_command import CircleCommand
from commands.rectangle_command import RectangleCommand
from commands.dimension_command import DimensionCommand, HorizontalDimensionCommand, VerticalDimensionCommand

# TODO: Move QActions to pythoncad_qt.py
# TODO: Deselect command on command_cancel (Esc) via signals


class CommandListModel(QtGui.QStandardItemModel):
    action_role = QtCore.Qt.UserRole + 1

    def roleNames(self):
        role_names = super(CommandListModel, self).roleNames()
        role_names[self.action_role] = 'action'
        return role_names

    def add_category(self, category):
        self.appendRow(category)


class CommandCategoryLabel(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super(CommandCategoryLabel, self).__init__(*args, **kwargs)
        self.setFlags(QtCore.Qt.NoItemFlags)
        self.setSelectable(False)

    def add_command(self, command):
        self.appendRow(command)


class CommandLabel(QtGui.QStandardItem):

    def __init__(self, *args, **kwargs):
        super(CommandLabel, self).__init__(*args, **kwargs)
        # TODO(chrisbura): Create default command icon
        # TODO(chrisbura): Use qrc
        # TODO(chrisbura): Customize in settings
        self.set_icon_path('images/commands/new.png')
        # TODO(chrisbura): Create default empty action
        # self.set_action(QtGui.QAction()))

    def set_label(self, label):
        self.setText(label)

    def set_icon_path(self, path):
        self.setIcon(QtGui.QIcon(path))

    def set_action(self, action):
        self.setData(action, CommandListModel.action_role)


class CommandPane(SidebarPane):

    command_started = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(CommandPane, self).__init__(parent)

        self.active_command = None

        self.model = CommandListModel()

        self.command_list = FilterableTreeView(self.model)
        self.command_list.set_filter_placeholder('Filter Commands')
        self.add_component(self.command_list)

        self.command_list.tree.clicked.connect(self.handle_click)

        self.setup_actions()

        # Drawing Category
        self.drawing_label = CommandCategoryLabel('Drawing')
        self.model.add_category(self.drawing_label)

        # Drawing -> Point
        point_command = CommandLabel('Point')
        point_command.set_action(self.point_action)
        self.drawing_label.add_command(point_command)

        # Drawing -> Segment
        segment_command = CommandLabel('Segment')
        segment_command.set_icon_path('images/commands/segment.png')
        segment_command.set_action(self.segment_action)
        self.drawing_label.add_command(segment_command)

        # Drawing -> Rectangle
        rectangle_command = CommandLabel('Rectangle')
        rectangle_command.set_icon_path('images/commands/rectangle.png')
        rectangle_command.set_action(self.rectangle_action)
        self.drawing_label.add_command(rectangle_command)

        # Drawing -> Circle
        circle_command = CommandLabel('Circle')
        circle_command.set_icon_path('images/commands/circle.png')
        circle_command.set_action(self.circle_action)
        self.drawing_label.add_command(circle_command)

        # Drawing -> Arc
        arc_command = CommandLabel('Arc')
        arc_command.set_icon_path('images/commands/arc.png')
        self.drawing_label.add_command(arc_command)

        # Drawing -> Ellipse
        ellipse_command = CommandLabel('Ellipse')
        ellipse_command.set_icon_path('images/commands/ellipse.png')
        self.drawing_label.add_command(ellipse_command)

        # Drawing -> Polygon
        polygon_command = CommandLabel('Polygon')
        polygon_command.set_icon_path('images/commands/polygon.png')
        self.drawing_label.add_command(polygon_command)

        # Drawing -> Polyline
        polyline_command = CommandLabel('Polyline')
        polyline_command.set_icon_path('images/commands/polyline.png')
        self.drawing_label.add_command(polyline_command)

        # Dimensioning Category
        self.dimension_label = CommandCategoryLabel('Dimensioning')
        self.model.add_category(self.dimension_label)

        # Dimensioning -> Dimension
        dimension_command = CommandLabel('Dimension')
        dimension_command.set_action(self.dimension_action)
        self.dimension_label.add_command(dimension_command)

        # Dimensioning -> Vertical Dimension
        vertical_dimension_command = CommandLabel('Vertical Dimension')
        vertical_dimension_command.set_action(self.vertical_dimension_action)
        self.dimension_label.add_command(vertical_dimension_command)

        # Dimensioning -> Horizontal Dimension
        horizontal_dimension_command = CommandLabel('Horizontal Dimension')
        horizontal_dimension_command.set_action(self.horizontal_dimension_action)
        self.dimension_label.add_command(horizontal_dimension_command)

        # Layer Category
        self.layer_label = CommandCategoryLabel('Layers')
        self.model.add_category(self.layer_label)

        # Layer -> Create New Layer
        new_layer_command = CommandLabel('Create New Layer')
        self.layer_label.add_command(new_layer_command)

        # Layer -> Rename Existing Layer
        rename_layer_command = CommandLabel('Rename Existing Layer')
        self.layer_label.add_command(rename_layer_command)

        # Layer -> Delete Existing Layer
        delete_layer_command = CommandLabel('Delete Existing Layer')
        self.layer_label.add_command(delete_layer_command)

        # Layer -> Open Layer Manager
        layer_manager_command = CommandLabel('Open Layer Manager')
        self.layer_label.add_command(layer_manager_command)

        # Constraint Category
        self.constraint_label = CommandCategoryLabel('Constraints')
        self.model.appendRow(self.constraint_label)

        # Constraint -> Fixed
        fixed_constraint_command = CommandLabel('Fixed')
        self.constraint_label.add_command(fixed_constraint_command)

        self.command_list.tree.expandAll()

    def setup_actions(self):
        # TODO(chrisbura): Investigate parent requirements for QActions
        # Point
        self.point_action = QtGui.QAction('Point', self.command_list)
        self.point_action.triggered.connect(
            partial(self.command_started.emit, PointCommand))

        # Segment
        self.segment_action = QtGui.QAction('Segment', self.command_list)
        self.segment_action.triggered.connect(
            partial(self.command_started.emit, SegmentCommand))

        # Rectangle
        self.rectangle_action = QtGui.QAction('Rectangle', self.command_list)
        self.rectangle_action.triggered.connect(
            partial(self.command_started.emit, RectangleCommand))

        # Circle
        self.circle_action = QtGui.QAction('Circle', self.command_list)
        self.circle_action.triggered.connect(
            partial(self.command_started.emit, CircleCommand))

        # Dimension
        self.dimension_action = QtGui.QAction('Dimension', self.command_list)
        self.dimension_action.triggered.connect(
            partial(self.command_started.emit, DimensionCommand))

        # Vertical Dimension
        self.vertical_dimension_action = QtGui.QAction('Vertical Dimension', self.command_list)
        self.vertical_dimension_action.triggered.connect(
            partial(self.command_started.emit, VerticalDimensionCommand))

        self.horizontal_dimension_action = QtGui.QAction('Horizontal Dimension', self.command_list)
        self.horizontal_dimension_action.triggered.connect(
            partial(self.command_started.emit, HorizontalDimensionCommand))

    def handle_click(self, index):
        if index.isValid():
            action = index.data(CommandListModel.action_role)

            try:
                action.trigger()
            except AttributeError:
                # No action is set on that index
                pass
