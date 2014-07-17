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

class CommandPane(SidebarPane):

    command_started = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(CommandPane, self).__init__(parent)

        self.active_command = None

        self.command_list = FilterableTreeView()
        self.command_list.set_filter_placeholder('Filter Commands')
        self.add_component(self.command_list)

        self.command_list.tree.clicked.connect(self.handle_click)

        # Setup Model Items
        # TODO: Find a cleaner way
        self.drawing_label = QtGui.QStandardItem('Drawing')
        self.drawing_label.setFlags(QtCore.Qt.NoItemFlags)
        self.drawing_label.setSelectable(False)
        self.command_list.model.appendRow(self.drawing_label)

        # Command: Point
        point_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Point')
        point_command.setData(
            QtGui.QAction('Point', self.command_list,
                triggered=partial(self.command_started.emit, PointCommand)),
            QtCore.Qt.UserRole,
            )
        self.drawing_label.appendRow(point_command)

        # Command: Segment
        segment_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/segment.png'), 'Segment')
        segment_command.setData(
            QtGui.QAction('Segment', self.command_list,
                triggered=partial(self.command_started.emit, SegmentCommand)),
            QtCore.Qt.UserRole,
            )
        self.drawing_label.appendRow(segment_command)

        rectangle_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/rectangle.png'), 'Rectangle')
        rectangle_command.setData(
            QtGui.QAction('Rectangle', self.command_list,
                triggered=partial(self.command_started.emit, RectangleCommand)),
            QtCore.Qt.UserRole,
            )
        self.drawing_label.appendRow(rectangle_command)

        # Command: Circle
        circle_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/circle.png'), 'Circle')
        circle_command.setData(
            QtGui.QAction('Circle', self.command_list,
                triggered=partial(self.command_started.emit, CircleCommand)),
            QtCore.Qt.UserRole,
            )
        self.drawing_label.appendRow(circle_command)

        arc_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/arc.png'), 'Arc')
        # self.drawing_label.appendRow(arc_command)
        ellipse_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/ellipse.png'), 'Ellipse')
        # self.drawing_label.appendRow(ellipse_command)
        polygon_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/polygon.png'), 'Polygon')
        # self.drawing_label.appendRow(polygon_command)
        polyline_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/polyline.png'), 'Polyline')
        # self.drawing_label.appendRow(polyline_command)

        self.dimension_label = QtGui.QStandardItem('Dimensioning')
        self.dimension_label.setFlags(QtCore.Qt.NoItemFlags)
        self.dimension_label.setSelectable(False)
        self.command_list.model.appendRow(self.dimension_label)

        dimension_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Dimension')
        dimension_command.setData(
            QtGui.QAction('Dimension', self.command_list,
                triggered=partial(self.command_started.emit, DimensionCommand)),
            QtCore.Qt.UserRole,
            )
        self.dimension_label.appendRow(dimension_command)

        vertical_dimension = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Vertical Dimension')
        vertical_dimension.setData(
            QtGui.QAction('Vertical Dimension', self.command_list,
                triggered=partial(self.command_started.emit, VerticalDimensionCommand)),
            QtCore.Qt.UserRole,
            )
        self.dimension_label.appendRow(vertical_dimension)

        horizontal_dimension = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Horizontal Dimension')
        horizontal_dimension.setData(
            QtGui.QAction('Horizontal Dimension', self.command_list,
                triggered=partial(self.command_started.emit, HorizontalDimensionCommand)),
            QtCore.Qt.UserRole,
            )
        self.dimension_label.appendRow(horizontal_dimension)

        self.layer_label = QtGui.QStandardItem('Layers')
        self.layer_label.setFlags(QtCore.Qt.NoItemFlags)
        self.layer_label.setSelectable(False)
        # self.command_list.model.appendRow(self.layer_label)

        new_layer_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Create new layer')
        # self.layer_label.appendRow(new_layer_command)
        rename_layer_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Rename existing layer')
        # self.layer_label.appendRow(rename_layer_command)
        delete_layer_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Delete existing layer')
        # self.layer_label.appendRow(delete_layer_command)
        layer_manager_command = QtGui.QStandardItem(QtGui.QIcon('images/commands/new.png'), 'Open layer manager')
        # self.layer_label.appendRow(layer_manager_command)

        self.command_list.tree.expandAll()

    def handle_click(self, index):
        if index.isValid():
            # TODO: Custom role type to prevent conflict?
            action = index.data(QtCore.Qt.UserRole)
            try:
                # Action is a QVariant, need to convert it back to a QAction
                # and then trigger it
                action.trigger()
            except AttributeError:
                # No action is set on that index
                pass
