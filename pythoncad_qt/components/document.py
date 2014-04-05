from PyQt4 import QtCore, QtGui

from components.base import ComponentBase, VerticalLayout, HorizontalLayout
from components.buttons import Button


class DocumentTitleLabel(QtGui.QLabel):
    pass


class TitleBar(HorizontalLayout, ComponentBase):

    layout_margins = QtCore.QMargins(0, 0, 11, 0)
    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.title = DocumentTitleLabel('Untitled')
        self.filename = QtGui.QLabel('filename.pdr')

        self.add_component(self.title)
        self.add_component(self.filename)
        self.add_component(Button('Save'))
        self.add_component(Button('Save As'))
        self.add_component(Button('Close'))

        self.add_stretch()

        self.expand = Button(QtGui.QIcon('images/maximize.png'), 'Expand')
        self.add_component(self.expand)

class Document(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

        self.titlebar = TitleBar(self)
        self.graphicsview = QtGui.QGraphicsView(self)

        self.add_component(self.titlebar)
        self.add_component(self.graphicsview)
