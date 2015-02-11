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

# This class is used to provide a basic signalling functionality for
# QGraphicsItems. Since they do not derive from QObject (for performance
# reasons), they do not have acccess to the Qt signal and slots system. None
# of the type checking or robustness available in the Qt system is available
# here. It is simply used for things like selected events and hover events.


class SimpleSignal(object):
    def __init__(self):
        self.connections = []

    def connect(self, slot):
        self.connections.append(slot)

    def disconnect(self, slot):
        self.connections.remove(slot)

    def emit(self, *args, **kwargs):
        for connection in self.connections:
            connection(*args, **kwargs)
