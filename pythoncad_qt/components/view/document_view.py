from PyQt4 import QtCore, QtGui


class DocumentView(QtGui.QGraphicsView):

    mouse_exit = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, *args, **kwargs):
        super(DocumentView, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)

        # Flip Y axis
        self.scale(1, -1)

        # Save default scale so that any zooming can be reset
        self.default_scale = self.transform()

        self.setRenderHint(QtGui.QPainter.Antialiasing)

    def leaveEvent(self, event):
        self.mouse_exit.emit(event)
        super(DocumentView, self).leaveEvent(event)

    def mousePressEvent(self, event):
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        if keyboard_modifiers == QtCore.Qt.ControlModifier and event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        super(DocumentView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        super(DocumentView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)

        scaling_factor = 1.15

        if event.delta() > 0:
            transform = QtGui.QTransform()
            transform.scale(scaling_factor, scaling_factor)
        else:
            transform = QtGui.QTransform()
            transform.scale(1.0 / scaling_factor, 1.0 / scaling_factor)

        self.setTransform(transform * self.transform())
