from PyQt4 import QtGui, QtCore

from .sidebar_pane import SidebarPane
from ..sidebar_widgets import FilterableTreeView


class CommandPane(SidebarPane):
    def __init__(self, parent=None):
        super(CommandPane, self).__init__(parent)

        self.command_list = FilterableTreeView()
        self.command_list.set_filter_placeholder('Filter Commands')
        self.add_component(self.command_list)

        # Setup Model Items
        # TODO: Find a cleaner way
        self.drawing_label = QtGui.QStandardItem('Drawing')
        self.drawing_label.setFlags(QtCore.Qt.NoItemFlags)
        self.drawing_label.setSelectable(False)
        self.command_list.model.appendRow(self.drawing_label)

        point_command = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), 'Point')
        self.drawing_label.appendRow(point_command)
        segment_command = QtGui.QStandardItem(QtGui.QIcon('images/segment.png'), 'Segment')
        self.drawing_label.appendRow(segment_command)
        circle_command = QtGui.QStandardItem(QtGui.QIcon('images/circle.png'), 'Circle')
        self.drawing_label.appendRow(circle_command)
        arc_command = QtGui.QStandardItem(QtGui.QIcon('images/arc.png'), 'Arc')
        self.drawing_label.appendRow(arc_command)
        ellipse_command = QtGui.QStandardItem(QtGui.QIcon('images/ellipse.png'), 'Ellipse')
        self.drawing_label.appendRow(ellipse_command)
        polygon_command = QtGui.QStandardItem(QtGui.QIcon('images/polygon.png'), 'Polygon')
        self.drawing_label.appendRow(polygon_command)
        polyline_command = QtGui.QStandardItem(QtGui.QIcon('images/polyline.png'), 'Polyline')
        self.drawing_label.appendRow(polyline_command)
        rectangle_command = QtGui.QStandardItem(QtGui.QIcon('images/rectangle.png'), 'Rectangle')
        self.drawing_label.appendRow(rectangle_command)

        self.layer_label = QtGui.QStandardItem('Layers')
        self.layer_label.setFlags(QtCore.Qt.NoItemFlags)
        self.layer_label.setSelectable(False)
        self.command_list.model.appendRow(self.layer_label)

        new_layer_command = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), 'Create new layer')
        self.layer_label.appendRow(new_layer_command)
        rename_layer_command = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), 'Rename existing layer')
        self.layer_label.appendRow(rename_layer_command)
        delete_layer_command = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), 'Delete existing layer')
        self.layer_label.appendRow(delete_layer_command)
        layer_manager_command = QtGui.QStandardItem(QtGui.QIcon('images/new.png'), 'Open layer manager')
        self.layer_label.appendRow(layer_manager_command)

        self.command_list.tree.expandAll()
