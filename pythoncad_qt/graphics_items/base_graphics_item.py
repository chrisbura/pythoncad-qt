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

    def hoverEnterEvent(self, event):
        super(BaseGraphicsItem, self).hoverEnterEvent(event)
        self.hover = True
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.pen_thickness))

    def hoverLeaveEvent(self, event):
        super(BaseGraphicsItem, self).hoverLeaveEvent(event)
        self.hover = False
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness))

    def paint(self, painter, option, widget):
        # Disable dotted selection rectangle
        option = QtGui.QStyleOptionGraphicsItem(option)
        option.state &= ~ QtGui.QStyle.State_Selected

        if self.hover:
            self.setPen(QtGui.QPen(QtCore.Qt.red, self.pen_thickness))
        else:
            self.setPen(QtGui.QPen(QtCore.Qt.black, self.pen_thickness))

        if self.isSelected():
            self.setPen(QtGui.QPen(QtCore.Qt.green, self.pen_thickness))

        if settings.DEBUG_SHAPES:
            painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
            painter.drawPath(self.shape())

        super(BaseGraphicsItem, self).paint(painter, option, widget)
