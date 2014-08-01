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

import copy


class HoverEvent(object):
    def __init__(self, event):
        self.event = event
        super(HoverEvent, self).__init__()


class HoverEnterEvent(HoverEvent):
    pass


class HoverLeaveEvent(HoverEvent):
    pass


class HoverMoveEvent(HoverEvent):
    pass


class HoverEventManager(object):
    def __init__(self):
        self.hover_items = []

    def process_hover(self, event, items):
        previous_items = copy.copy(self.hover_items)

        for item in items:
            if item not in self.hover_items:
                self.hover_items.append(item)
                hover_event = HoverEnterEvent(event)
            else:
                previous_items.remove(item)
                hover_event = HoverMoveEvent(event)

            item.hover_event(hover_event)

        for item in previous_items:
            hover_event = HoverLeaveEvent(event)

            item.hover_event(hover_event)

            self.hover_items.remove(item)
