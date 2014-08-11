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

from PyQt4 import QtCore

DEBUG = True
DEBUG_SHAPES = False
DEBUG_BOUNDING_RECT = False
DEBUG_SHAPES_COLOUR = QtCore.Qt.cyan
DEBUG_DIMENSION_ZONES = True
DEBUG_SNAP_LINES = False
DEBUG_OUTLINE_SCENEITEMS = False

STYLESHEET = 'stylesheets/pythoncad_qt.css'

DEFAULT_COLOUR = QtCore.Qt.black
ITEM_PEN_THICKNESS = 2
HIGHLIGHT_COLOUR = QtCore.Qt.red
SELECTED_COLOUR = QtCore.Qt.green
JOIN_STYLE = QtCore.Qt.MiterJoin
LINE_STYLE = QtCore.Qt.SolidLine

GRID_SPACING = 20
DRAW_GRID = True
DRAW_AXES = True

UNITS = 'mm'

SNAP_SNAPLINES = True
SNAP_CENTER_POINTS = True
SNAP_ENDPOINTS = True
SNAP_MIDPOINTS = True
SNAP_QUARTER_POINTS = True
