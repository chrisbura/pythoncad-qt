from PyQt4 import QtCore, QtGui

import settings


class FilledShapeMixin(object):
    def __init__(self, *args, **kwargs):
        super(FilledShapeMixin, self).__init__(*args, **kwargs)
        self.setBrush(self.default_colour)

    def paint(self, painter, option, widget):
        super(FilledShapeMixin, self).paint(painter, option, widget)
        self.setBrush(self.item_colour())
        if self.isSelected():
            self.setBrush(self.selected_colour)


class BaseGraphicsItem(object):

    default_colour = settings.DEFAULT_COLOUR
    hover_colour = settings.HIGHLIGHT_COLOUR
    selected_colour = settings.SELECTED_COLOUR
    pen_thickness = settings.ITEM_PEN_THICKNESS

    def __init__(self, *args, **kwargs):
        super(BaseGraphicsItem, self).__init__(*args, **kwargs)
        self.hover = False
        self.setPen(QtGui.QPen(self.default_colour, self.pen_thickness, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

    def hoverEnterEvent(self, event):
        super(BaseGraphicsItem, self).hoverEnterEvent(event)
        self.hover = True

    def hoverLeaveEvent(self, event):
        super(BaseGraphicsItem, self).hoverLeaveEvent(event)
        self.hover = False

    def item_colour(self):
        if self.hover:
            return self.hover_colour
        return self.default_colour

    def paint(self, painter, option, widget):
        # Disable dotted selection rectangle
        option = QtGui.QStyleOptionGraphicsItem(option)
        option.state &= ~ QtGui.QStyle.State_Selected

        self.setPen(QtGui.QPen(self.item_colour(), self.pen_thickness))

        if self.isSelected():
            self.setPen(QtGui.QPen(self.selected_colour, self.pen_thickness))

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(settings.DEBUG_SHAPES_COLOUR))
            painter.drawPath(self.shape())

        super(BaseGraphicsItem, self).paint(painter, option, widget)
