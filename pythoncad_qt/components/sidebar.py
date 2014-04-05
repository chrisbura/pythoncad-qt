from PyQt4 import QtCore, QtGui

from .base import VerticalLayout, ComponentBase


class SidebarPaneSelector(QtGui.QComboBox):
    def __init__(self, *args, **kwargs):
        super(SidebarPaneSelector, self).__init__(*args, **kwargs)

        self.item_delegate = QtGui.QStyledItemDelegate()
        self.setItemDelegate(self.item_delegate)


class SidebarPaneStack(QtGui.QStackedWidget):
    pass


class Sidebar(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(Sidebar, self).__init__(*args, **kwargs)

        self.pane_selector = SidebarPaneSelector()
        self.add_component(self.pane_selector)

        self.pane_stack = SidebarPaneStack()
        self.add_component(self.pane_stack)

        self.pane_selector.currentIndexChanged.connect(
            self.pane_stack.setCurrentIndex
        )

    def add_pane(self, title, pane):
        # TODO: Error checking
        self.pane_selector.addItem(title)
        self.pane_stack.addWidget(pane)
