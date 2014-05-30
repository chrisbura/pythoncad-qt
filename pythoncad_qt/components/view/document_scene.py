import math

from PyQt4 import QtCore, QtGui

from sympy.geometry import Point

from graphics_items.point_graphics_item import PointGraphicsItem
from commands.inputs import PointInput


class DocumentScene(QtGui.QGraphicsScene):

    mouse_move = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)
    active_command_click = QtCore.pyqtSignal(object)
    entity_added = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(DocumentScene, self).__init__(*args, **kwargs)

        # Arguments are x, y, width, height
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.grid_spacing = 20

        # Commands
        self.active_command = None
        self.preview_item = None

        self.active_command_click.connect(self.handle_click)

    def mouseReleaseEvent(self, event):
        # Split mouseReleaseEvent using signals to prevent large method
        if event.button() == QtCore.Qt.LeftButton and self.active_command is not None:
            self.active_command_click.emit(event)

        super(DocumentScene, self).mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        # Cancel active command on esc
        # TODO: Handle focus, click command and bring focus to QGraphicsScene
        if event.key() == QtCore.Qt.Key_Escape and self.active_command is not None:
            # TODO: Emit command canceled signal
            # TODO: deselect command on cancel
            self.active_command = None
            print 'Cancel'

    def handle_click(self, event):
        command = self.active_command
        current_input = command.inputs[command.active_input]

        if isinstance(current_input, PointInput):
            item = self.itemAt(event.scenePos())
            if item is not None and isinstance(item, PointGraphicsItem):
                current_input.value = Point(item.entity.x, item.entity.y)
            else:
                current_input.value = Point(event.scenePos().x(), event.scenePos().y())

        if command.has_preview and (command.active_input == command.preview_start):
            self.preview_item = command.preview_item()
            self.mouse_move.connect(self.preview_item.update)
            self.addItem(self.preview_item)

        command.active_input = command.active_input + 1

        if command.active_input == len(command.inputs):
            # Get QGraphics*Item
            graphics_item = command.apply_command()
            # self.entity_added.emit(graphics_item.entity)
            self.addItem(graphics_item)
            self.active_command = None

            # Remove the preview item from the scene
            if self.preview_item is not None:
                self.removeItem(self.preview_item)
                self.preview_item = None

    def drawBackground(self, painter, rect):
        painter.save()

        # Grid Colours
        # TODO: Move to settings
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200, 100)))

        # TODO: Allow toggling

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

        # Axis
        # TODO: Allow toggling
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(rect.left(), 0, rect.right(), 0)
        painter.drawLine(0, rect.top(), 0, rect.bottom())

        painter.restore()

    def mouseMoveEvent(self, event):
        super(DocumentScene, self).mouseMoveEvent(event)
        self.mouse_move.emit(event)