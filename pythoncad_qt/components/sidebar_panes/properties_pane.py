from PyQt4 import QtGui

from .sidebar_pane import SidebarPane

class PropertiesPane(SidebarPane):
    def __init__(self, parent=None):
        super(PropertiesPane, self).__init__(parent)
        self.add_component(QtGui.QLabel('Properties'), alignment=QtCore.Qt.AlignTop)

