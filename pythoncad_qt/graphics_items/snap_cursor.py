
from PyQt4 import QtGui, QtCore


class SnapCursor(QtGui.QGraphicsRectItem):
    def __init__(self, x, y):

        self.width = 10
        self.x, self.y = x, y

        super(SnapCursor, self).__init__(self.get_rect(x, y))

        self.pen = QtGui.QPen()
        self.pen.setColor(QtCore.Qt.magenta)
        self.pen.setWidth(2)
        self.setPen(self.pen)

    def set_position(self, x, y):
        self.setRect(self.get_rect(x, y))

    def get_rect(self, x, y):
        return QtCore.QRectF(
            x - self.width / 2,
            y - self.width / 2,
            self.width,
            self.width
        )
