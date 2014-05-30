from PyQt4 import QtCore, QtGui

import settings


class BaseGraphicsItem(object):
    def __init__(self, *args, **kwargs):
        super(BaseGraphicsItem, self).__init__(*args, **kwargs)
        self.hover = False
        self.pen_thickness = 1
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness, QtCore.Qt.SolidLine))
        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        # setBrush comes from QAbstractGraphicsShapeItem, as a result
        # QGraphicsLineItem won't have it
        try:
            self.setBrush(QtCore.Qt.black)
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
            pen_colour = QtCore.Qt.red
        else:
            pen_colour = QtCore.Qt.black

        self.setPen(QtGui.QPen(pen_colour, self.pen_thickness))

        # See note about QAbstractGraphicsShapeItem above
        try:
            self.setBrush(pen_colour)
        except AttributeError:
            pass

        if self.isSelected():
            self.setPen(QtGui.QPen(QtCore.Qt.green, self.pen_thickness))
            try:
                self.setBrush(QtCore.Qt.green)
            except AttributeError:
                pass

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
            painter.drawPath(self.shape())

        super(BaseGraphicsItem, self).paint(painter, option, widget)
