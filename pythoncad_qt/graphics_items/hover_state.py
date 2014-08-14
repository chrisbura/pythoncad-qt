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

from hover_event_manager import HoverEnterEvent, HoverLeaveEvent, HoverMoveEvent


class HoverState(object):
    def hover_event(self, event):
        if type(event) == HoverEnterEvent:
            self.hover_enter_event(event)

        if type(event) == HoverLeaveEvent:
            self.hover_leave_event(event)

        if type(event) == HoverMoveEvent:
            self.hover_move_event(event)

    def hover_enter_event(self, event):
        self.update()

    def hover_leave_event(self, event):
        self.update()

    def hover_move_event(self, event):
        self.update()