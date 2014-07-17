#
# PythonCAD-Qt
# Copyright (C) 2014 Christopher Bura
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

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
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    def leaveEvent(self, event):
        self.mouse_exit.emit(event)
        super(DocumentView, self).leaveEvent(event)

    def mousePressEvent(self, event):
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        if keyboard_modifiers == QtCore.Qt.ControlModifier and event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        super(DocumentView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(DocumentView, self).mouseReleaseEvent(event)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

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
