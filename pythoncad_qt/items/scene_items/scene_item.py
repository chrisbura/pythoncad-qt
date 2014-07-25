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

from PyQt4 import QtCore, QtGui

import settings


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


class SceneItem(object):

    default_colour = settings.DEFAULT_COLOUR
    hover_colour = settings.HIGHLIGHT_COLOUR
    selected_colour = settings.SELECTED_COLOUR
    pen_thickness = settings.ITEM_PEN_THICKNESS
    pen_join_style = settings.JOIN_STYLE

    def __init__(self, *args, **kwargs):
        super(SceneItem, self).__init__(*args, **kwargs)
        self.hover = False

        # Pens
        self.default_pen = BasePen(self.default_colour)
        self.hover_pen = BasePen(self.hover_colour)
        self.selected_pen = BasePen(self.selected_colour)

        # Brushes
        self.default_brush = BaseBrush(self.default_colour)
        self.hover_brush = BaseBrush(self.hover_colour)
        self.selected_brush = BaseBrush(self.selected_colour)

        self.setPen(self.default_pen)

        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

    def hoverEnterEvent(self, event):
        super(SceneItem, self).hoverEnterEvent(event)
        self.hover = True

    def hoverLeaveEvent(self, event):
        super(SceneItem, self).hoverLeaveEvent(event)
        self.hover = False

    def active_pen(self):
        if self.hover:
            return self.hover_pen
        return self.default_pen

    def active_brush(self):
        if self.hover:
            return self.hover_brush
        return self.default_brush

    def paint(self, painter, option, widget):
        # Disable dotted selection rectangle
        option = QtGui.QStyleOptionGraphicsItem(option)
        option.state &= ~ QtGui.QStyle.State_Selected

        self.setPen(self.active_pen())

        if self.isSelected():
            self.setPen(self.selected_pen)

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())

        if settings.DEBUG_BOUNDING_RECT:
            bounding_rect = QtGui.QPainterPath()
            bounding_rect.addRect(self.boundingRect())
            painter.drawPath(bounding_rect)

        super(SceneItem, self).paint(painter, option, widget)
