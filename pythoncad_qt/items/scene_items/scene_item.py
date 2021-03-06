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

import sip
from PyQt4 import QtCore, QtGui

import settings
from hover_event_manager import HoverState
from .simple_signal import SimpleSignal


class UnselectableMixin(object):
    def __init__(self, *args, **kwargs):
        super(UnselectableMixin, self).__init__(*args, **kwargs)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)


class FilledShapeMixin(object):
    def __init__(self, *args, **kwargs):
        super(FilledShapeMixin, self).__init__(*args, **kwargs)
        self.setBrush(self.default_brush)

    def paint(self, painter, option, widget):
        super(FilledShapeMixin, self).paint(painter, option, widget)
        self.setBrush(self.active_brush())
        if self.isSelected():
            self.setBrush(self.selected_brush)


class BaseBrush(QtGui.QBrush):
    pass


class BasePen(QtGui.QPen):
    def __init__(self, color, *args, **kwargs):
        super(BasePen, self).__init__(*args, **kwargs)
        self.setWidth(settings.ITEM_PEN_THICKNESS)
        self.setJoinStyle(settings.JOIN_STYLE)
        self.setStyle(settings.LINE_STYLE)
        self.setColor(color)


class HoverMixin(object):

    hover_colour = settings.HIGHLIGHT_COLOUR

    def __init__(self, *args, **kwargs):
        super(HoverMixin, self).__init__(*args, **kwargs)
        self.hover = False
        self.hover_pen = BasePen(self.hover_colour)
        self.hover_brush = BaseBrush(self.hover_colour)

        self.hover_enter_signal = SimpleSignal()
        self.hover_leave_signal = SimpleSignal()

    def hover_enter_event(self, event):
        self.hover = True
        self.hover_enter_signal.emit(event)
        super(HoverMixin, self).hover_enter_event(event)

    def hover_leave_event(self, event):
        self.hover = False
        self.hover_leave_signal.emit(event)
        super(HoverMixin, self).hover_leave_event(event)

    def active_pen(self):
        if self.hover:
            return self.hover_pen
        return self.default_pen

    def active_brush(self):
        if self.hover:
            return self.hover_brush
        return self.default_brush


class SelectableMixin(object):

    selected_colour = settings.SELECTED_COLOUR

    def __init__(self, *args, **kwargs):
        super(SelectableMixin, self).__init__(*args, **kwargs)
        self.selected_pen = BasePen(self.selected_colour)
        self.selected_brush = BaseBrush(self.selected_colour)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        self.selected_signal = SimpleSignal()
        self.unselected_signal = SimpleSignal()

    def paint(self, painter, option, widget):
        # Disable dotted selection rectangle
        option = QtGui.QStyleOptionGraphicsItem(option)
        option.state &= ~ QtGui.QStyle.State_Selected

        if self.isSelected():
            self.setPen(self.selected_pen)

        super(SelectableMixin, self).paint(painter, option, widget)

    def on_selected(self):
        self.selected_signal.emit()
        if settings.DEBUG_SELECTION:
            # TODO(chrisbura): Print item information
            print 'Selected'

    def on_unselected(self):
        self.unselected_signal.emit()
        if settings.DEBUG_SELECTION:
            # TODO(chrisbura): Print item information
            print 'Unselected'

    def itemChange(self, change, value):
        # TODO(chrisbura): Find difference between ItemSelectedHasChanged and ItemSelectedChange
        if change == QtGui.QGraphicsItem.ItemSelectedHasChanged and value is not None:
            if value == True:
                self.on_selected()
            else:
                self.on_unselected()

        # itemChange and setParentItem causes error in PyQt4
        # TODO: Test with PySide and PyQt5
        # See http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        result =  super(SelectableMixin, self).itemChange(change, value)
        if isinstance(result, QtGui.QGraphicsItem):
            result = sip.cast(result, QtGui.QGraphicsItem)
        return result


class DefaultPenMixin(object):

    default_colour = settings.DEFAULT_COLOUR

    def __init__(self, *args, **kwargs):
        super(DefaultPenMixin, self).__init__(*args, **kwargs)
        self.default_pen = BasePen(self.default_colour)
        self.default_brush = BaseBrush(self.default_colour)

    def active_pen(self):
        return self.default_pen

    def active_brush(self):
        return self.default_brush

    def paint(self, painter, *args, **kwargs):
        self.setPen(self.active_pen())
        super(DefaultPenMixin, self).paint(painter, *args, **kwargs)


class ShapeDebugMixin(object):
    def paint(self, painter, *args, **kwargs):
        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())

        if settings.DEBUG_BOUNDING_RECT:
            bounding_rect = QtGui.QPainterPath()
            bounding_rect.addRect(self.boundingRect())
            painter.drawPath(bounding_rect)

        super(ShapeDebugMixin, self).paint(painter, *args, **kwargs)


class MovableMixin(object):
    def __init__(self, *args, **kwargs):
        super(MovableMixin, self).__init__(*args, **kwargs)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.position_changed = SimpleSignal()


class CoordinateSnapMixin(object):
    def __init__(self, *args, **kwargs):
        super(CoordinateSnapMixin, self).__init__(*args, **kwargs)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange and self.scene():

            # If Left mouse + alt is pressed then don't snap
            button = QtGui.QApplication.mouseButtons() == QtCore.Qt.LeftButton
            modifier = QtGui.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier

            if button and modifier:
                self.position_changed.emit(value)
                return super(CoordinateSnapMixin, self).itemChange(change, value)

            # Get all items under the mouse
            # TODO: Use try instead of isinstance
            # TODO: Add priority
            # TODO: Use childItems
            items = [x for x in self.scene().items(value) if isinstance(x, SnapsCoordinates) and x.parentItem() is not self]

            for item in items:
                value = item.snap_coordinate(value)

            self.position_changed.emit(value)

        # itemChange and setParentItem causes error in PyQt4
        # TODO: Test with PySide and PyQt5
        # See http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        result =  super(CoordinateSnapMixin, self).itemChange(change, value)
        if isinstance(result, QtGui.QGraphicsItem):
            result = sip.cast(result, QtGui.QGraphicsItem)
        return result


class SnapsCoordinates(object):
    def __init__(self, *args, **kwargs):
        super(SnapsCoordinates, self).__init__(*args, **kwargs)

    def snap_coordinate(self, value):
        pass


# TODO: Clean up...
class SceneItem(HoverMixin, HoverState, DefaultPenMixin, SelectableMixin, ShapeDebugMixin):
    pass
