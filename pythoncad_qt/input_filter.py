#
# PythonCAD-Qt
# Copyright (C) 2015 Christopher Bura
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


# TODO: Add priority
class Filter(object):
    def __init__(self, *args, **kwargs):
        self._active = False
        self.filter_dict = {}

    def set_active(self, value):
        self._active = value

    def is_active(self):
        return self._active


class AxisLockFilter(Filter):
    pass


class HorizontalAxisLockFilter(AxisLockFilter):
    def __init__(self, value, *args, **kwargs):
        super(HorizontalAxisLockFilter, self).__init__(*args, **kwargs)
        self.filter_dict = {'y': value}


class VerticalAxisLockFilter(AxisLockFilter):
    def __init__(self, value, *args, **kwargs):
        super(VerticalAxisLockFilter, self).__init__(*args, **kwargs)
        self.filter_dict = {'x': value}


class InputFilter(QtCore.QObject):

    # Click signals
    raw_click = QtCore.pyqtSignal(float, float)
    filtered_click = QtCore.pyqtSignal(float, float)

    # Move Signals
    raw_move = QtCore.pyqtSignal(float, float)
    filtered_move = QtCore.pyqtSignal(float, float)

    def __init__(self, *args, **kwargs):
        super(InputFilter, self).__init__(*args, **kwargs)
        self.filters = []

    def active_filters(self):
        for input_filter in self.filters:
            if input_filter.is_active():
                yield input_filter

    def add_filter(self, input_filter):
        self.filters.append(input_filter)

    # TODO: Recurse to get a list of filters from root item, use here and remove
    def add_filters(self, items):
        # TODO: Simplify
        for item in items:
            for child in item.traverse():
                for input_filter in child.filters():
                    self.add_filter(input_filter)

    def apply_filters(self, coordinates):
        # TODO: Only works with coordinate filters
        # TODO: Test performance with thousands of items
        for active_filter in self.active_filters():
            coordinates.update(active_filter.filter_dict)
        return coordinates

    def handle_click(self, x, y, *args, **kwargs):
        coordinates = {'x': x, 'y': y}

        self.raw_click.emit(coordinates['x'], coordinates['y'])
        coordinates = self.apply_filters(coordinates)
        self.filtered_click.emit(coordinates['x'], coordinates['y'])

    def handle_move(self, event):
        coordinates = {'x': event.scenePos().x(), 'y': event.scenePos().y()}

        # TODO: raw_move can be used to ignore filters while adding items
        self.raw_move.emit(coordinates['x'], coordinates['y'])
        coordinates = self.apply_filters(coordinates)
        self.filtered_move.emit(coordinates['x'], coordinates['y'])
