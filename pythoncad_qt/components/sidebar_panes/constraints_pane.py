from PyQt4 import QtGui

from .sidebar_pane import SidebarPane


class ConstraintsPane(SidebarPane):
    def __init__(self, parent=None):
        super(ConstraintsPane, self).__init__(parent)
        self.add_component(QtGui.QLabel('Constraints'), alignment=QtCore.Qt.AlignTop)
