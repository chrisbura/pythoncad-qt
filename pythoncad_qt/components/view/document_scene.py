import math

from PyQt4 import QtCore, QtGui

import settings
from graphics_items.snap_cursor import SnapCursor


class DocumentScene(QtGui.QGraphicsScene):

    mouse_move = QtCore.pyqtSignal(float, float)
    mouse_moved = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)
    mouse_click = QtCore.pyqtSignal(float, float, list)
    entity_added = QtCore.pyqtSignal(object)
    command_cancelled = QtCore.pyqtSignal()
    lock_input = QtCore.pyqtSignal(object)
    release_input = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(DocumentScene, self).__init__(*args, **kwargs)

        # Arguments are x, y, width, height
        self.setSceneRect(-10000, -10000, 20000, 20000)

        # Grid
        self.setting_draw_grid = settings.DRAW_GRID
        self.grid_spacing = settings.GRID_SPACING

        # Axes
        self.setting_draw_axes = settings.DRAW_AXES

        # TODO: Proper cursor
        self.cursor = SnapCursor(0, 0)
        self.cursor.hide()
        self.addItem(self.cursor)

        self.input_snapped = False
        self.horizontal_snapped = False
        self.horizontal_value = None
        self.vertical_snapped = False
        self.vertical_value = None

        self.composite_items = []

    def reset_scene(self):
        # TODO: Reset scene properly
        self.clear()

    def lock_point(self, point):
        self.input_snapped = True
        # TODO: Proper cursor handling
        self.cursor.set_position(point.x, point.y)
        self.lock_input.emit(point)

    def unlock_point(self):
        self.input_snapped = False
        self.horizontal_snapped = False
        self.vertical_snapped = False
        self.horizontal_value = None
        self.vertical_value = None
        self.release_input.emit()

    def add_composite_item(self, composite_items):
        self.composite_items.append(composite_items)
        for composite_item in composite_items:
            for item in composite_item.children:
                self.addItem(item)
                item.parent.hover_enter.connect(self.lock_point)
                item.parent.hover_leave.connect(self.unlock_point)
                item.parent.lock_horizontal.connect(self.lock_horizontal)
                item.parent.lock_vertical.connect(self.lock_vertical)

    def lock_horizontal(self, y):
        self.horizontal_snapped = True
        self.horizontal_value = y

    def lock_vertical(self, x):
        self.vertical_snapped = True
        self.vertical_value = x

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x, y = event.scenePos().x(), event.scenePos().y()

            if self.horizontal_snapped:
                y = self.horizontal_value

            if self.vertical_snapped:
                x = self.vertical_value

            self.mouse_click.emit(x, y, self.items(event.scenePos()))

        super(DocumentScene, self).mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        # Cancel active command on esc
        # TODO: Handle focus, click command and bring focus to QGraphicsScene
        if event.key() == QtCore.Qt.Key_Escape:
            self.command_cancelled.emit()

        # Delete Selected Items
        selected_items = self.selectedItems()
        if event.key() == QtCore.Qt.Key_Delete and len(selected_items) > 0:
            items_to_remove = set(selected_items)
            for item in selected_items:
                # Create list of unique items to remove using set.union
                # items_to_remove ends up being made up of selectedItems and all
                # the siblings of those items
                items_to_remove = items_to_remove | set(item.parent.children)

            # Remove items
            for item in items_to_remove:
                self.removeItem(item)

        super(DocumentScene, self).keyReleaseEvent(event)

    def drawBackground(self, painter, rect):
        if self.setting_draw_grid:
            self.draw_grid(painter, rect)

        if self.setting_draw_axes:
            self.draw_axes(painter, rect)

    def toggle_grid(self):
        self.setting_draw_grid = not self.setting_draw_grid
        self.invalidate(self.sceneRect(), QtGui.QGraphicsScene.BackgroundLayer)

    def draw_grid(self, painter, rect):
        painter.save()

        # Grid Colours
        # TODO: Move to settings
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200, 100)))

        # Horizontal Grid
        top_count = -1 * int(math.floor(rect.top() / self.grid_spacing))
        bottom_count = int(math.ceil(rect.bottom() / self.grid_spacing))

        for i in xrange(bottom_count):
            y = i * self.grid_spacing
            painter.drawLine(rect.left(), y, rect.right(), y)

        for i in xrange(top_count):
            y = i * -self.grid_spacing
            painter.drawLine(rect.left(), y, rect.right(), y)

        # Vertical Grid
        left_count = -1 * int(math.floor(rect.left() / self.grid_spacing))
        right_count = int(math.ceil(rect.right() / self.grid_spacing))

        for i in xrange(left_count):
            x = i * -self.grid_spacing
            painter.drawLine(x, rect.top(), x, rect.bottom())

        for i in xrange(right_count):
            x = i * self.grid_spacing
            painter.drawLine(x, rect.top(), x, rect.bottom())

        painter.restore()

    def toggle_axes(self):
        self.setting_draw_axes = not self.setting_draw_axes
        self.invalidate(self.sceneRect(), QtGui.QGraphicsScene.BackgroundLayer)

    def draw_axes(self, painter, rect):
        painter.save()
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(rect.left(), 0, rect.right(), 0)
        painter.drawLine(0, rect.top(), 0, rect.bottom())
        painter.restore()

    def mouseMoveEvent(self, event):
        super(DocumentScene, self).mouseMoveEvent(event)
        self.mouse_moved.emit(event)
        x, y = event.scenePos().x(), event.scenePos().y()

        if self.horizontal_snapped:
            y = self.horizontal_value

        if self.vertical_snapped:
            x = self.vertical_value

        self.mouse_move.emit(x, y)

        # TODO: Only show cursor when snapped
        if not self.input_snapped:
            self.cursor.set_position(x, y)

    def focusInEvent(self, event):
        self.cursor.show()

    def focusOutEvent(self, event):
        self.cursor.hide()
