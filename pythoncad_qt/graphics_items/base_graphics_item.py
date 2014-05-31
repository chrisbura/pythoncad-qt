from PyQt4 import QtCore, QtGui

import settings


class BaseGraphicsItem(object):
    def __init__(self, *args, **kwargs):
        super(BaseGraphicsItem, self).__init__(*args, **kwargs)
        self.hover = False
        self.setPen(QtGui.QPen(settings.ITEM_COLOUR, settings.ITEM_PEN_THICKNESS, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        # setBrush comes from QAbstractGraphicsShapeItem, as a result
        # QGraphicsLineItem won't have it
        try:
            self.setBrush(settings.ITEM_COLOUR)
        except AttributeError:
            pass

    def hoverEnterEvent(self, event):
        super(BaseGraphicsItem, self).hoverEnterEvent(event)
        self.hover = True

    def hoverLeaveEvent(self, event):
        super(BaseGraphicsItem, self).hoverLeaveEvent(event)
        self.hover = False

    def paint(self, painter, option, widget):
        # Disable dotted selection rectangle
        option = QtGui.QStyleOptionGraphicsItem(option)
        option.state &= ~ QtGui.QStyle.State_Selected

        if self.hover:
            pen_colour = settings.HIGHLIGHT_COLOUR
        else:
            pen_colour = settings.ITEM_COLOUR

        self.setPen(QtGui.QPen(pen_colour, settings.ITEM_PEN_THICKNESS))

        # See note about QAbstractGraphicsShapeItem above
        try:
            self.setBrush(pen_colour)
        except AttributeError:
            pass

        if self.isSelected():
            self.setPen(QtGui.QPen(settings.SELECTED_COLOUR, settings.ITEM_PEN_THICKNESS))
            try:
                self.setBrush(settings.SELECTED_COLOUR)
            except AttributeError:
                pass

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())

        super(BaseGraphicsItem, self).paint(painter, option, widget)
