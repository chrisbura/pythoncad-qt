from PyQt4 import QtCore, QtGui

import settings


class BaseGraphicsItem(object):

    item_colour = settings.ITEM_COLOUR
    hover_colour = settings.HIGHLIGHT_COLOUR
    selected_colour = settings.SELECTED_COLOUR
    pen_thickness = settings.ITEM_PEN_THICKNESS

    def __init__(self, *args, **kwargs):
        super(BaseGraphicsItem, self).__init__(*args, **kwargs)
        self.hover = False
        self.setPen(QtGui.QPen(self.item_colour, self.pen_thickness, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        # setBrush comes from QAbstractGraphicsShapeItem, as a result
        # QGraphicsLineItem won't have it
        try:
            self.setBrush(self.item_colour)
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
            pen_colour = self.hover_colour
        else:
            pen_colour = self.item_colour

        self.setPen(QtGui.QPen(pen_colour, self.pen_thickness))

        # See note about QAbstractGraphicsShapeItem above
        try:
            self.setBrush(pen_colour)
        except AttributeError:
            pass

        if self.isSelected():
            self.setPen(QtGui.QPen(self.selected_colour, self.pen_thickness))
            try:
                self.setBrush(self.selected_colour)
            except AttributeError:
                pass

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())

        super(BaseGraphicsItem, self).paint(painter, option, widget)
