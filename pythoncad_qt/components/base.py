from PyQt4 import QtCore, QtGui

from constants import MARGINS_ZERO


class Layout(object):
    layout_margins = MARGINS_ZERO
    layout_spacing = 0

    def __init__(self, *args, **kwargs):
        super(Layout, self).__init__(*args, **kwargs)
        # TODO: Error checking
        self.layout.setContentsMargins(self.layout_margins)
        self.layout.setSpacing(self.layout_spacing)

    def add_component(self, *args, **kwargs):
        # TODO: Error checking
        self.layout.addWidget(*args, **kwargs)

    def add_stretch(self):
        self.layout.addStretch()


class VerticalLayout(Layout):
    def __init__(self, *args, **kwargs):
        self.layout = QtGui.QVBoxLayout()
        super(VerticalLayout, self).__init__(*args, **kwargs)


class HorizontalLayout(Layout):
    def __init__(self, *args, **kwargs):
        self.layout = QtGui.QHBoxLayout()
        super(HorizontalLayout, self).__init__(*args, **kwargs)


class StyleableWidget(QtGui.QWidget):
    def paintEvent(self, event):
        # Needed to allow styling subclassed QWidgets
        # See http://qt-project.org/wiki/How_to_Change_the_Background_Color_of_QWidget
        option = QtGui.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter()
        painter.begin(self)
        self.style().drawPrimitive(QtGui.QStyle.PE_Widget, option, painter, self)


class ComponentBase(StyleableWidget):
    def __init__(self, *args, **kwargs):
        super(ComponentBase, self).__init__(*args, **kwargs)
        # TODO: Error checking
        self.setLayout(self.layout)
