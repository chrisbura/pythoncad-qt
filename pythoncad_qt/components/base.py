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

from PyQt4 import QtCore, QtGui

from .constants import MARGINS_ZERO


class Layout(object):
    layout_margins = MARGINS_ZERO
    layout_spacing = 0

    def __init__(self, *args, **kwargs):
        super(Layout, self).__init__(*args, **kwargs)
        # TODO: Error checking
        self.layout.setContentsMargins(self.layout_margins)
        self.layout.setSpacing(self.layout_spacing)
        self.setLayout(self.layout)

    def add_component(self, *args, **kwargs):
        # TODO: Error checking
        self.layout.addWidget(*args, **kwargs)

    def add_stretch(self):
        self.layout.addStretch()


class VerticalLayout(Layout):
    def __init__(self, *args, **kwargs):
        self.layout = QtGui.QVBoxLayout()
        super(VerticalLayout, self).__init__(*args, **kwargs)


class HorizontalLayout(Layout):
    def __init__(self, *args, **kwargs):
        self.layout = QtGui.QHBoxLayout()
        super(HorizontalLayout, self).__init__(*args, **kwargs)


class StyleableWidget(QtGui.QWidget):
    def paintEvent(self, event):
        # Needed to allow styling subclassed QWidgets
        # See http://qt-project.org/wiki/How_to_Change_the_Background_Color_of_QWidget
        option = QtGui.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter()
        painter.begin(self)
        self.style().drawPrimitive(QtGui.QStyle.PE_Widget, option, painter, self)


class ComponentBase(StyleableWidget):
    def __init__(self, *args, **kwargs):
        super(ComponentBase, self).__init__(*args, **kwargs)
