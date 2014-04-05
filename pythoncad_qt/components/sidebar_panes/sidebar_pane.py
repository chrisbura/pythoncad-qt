from PyQt4 import QtCore

from ..constants import MARGINS_TEN
from components.base import VerticalLayout, ComponentBase


class SidebarPane(VerticalLayout, ComponentBase):
    layout_margins = QtCore.QMargins(9, 9, 9, 9)
    layout_spacing = 6
