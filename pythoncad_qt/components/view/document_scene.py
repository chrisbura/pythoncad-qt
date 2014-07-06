import math

from PyQt4 import QtCore, QtGui

from settings import GRID_SPACING


class DocumentScene(QtGui.QGraphicsScene):

    mouse_move = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)
    active_command_click = QtCore.pyqtSignal(object, list)
    entity_added = QtCore.pyqtSignal(object)
    command_cancelled = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(DocumentScene, self).__init__(*args, **kwargs)

        # Arguments are x, y, width, height
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.grid_spacing = GRID_SPACING

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.active_command_click.emit(event, self.items(event.scenePos()))

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
