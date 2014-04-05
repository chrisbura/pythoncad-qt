from ..sidebar_widgets import FilterableTreeView
from .sidebar_pane import SidebarPane


class OutlinePane(SidebarPane):
    def __init__(self, parent=None):
        super(OutlinePane, self).__init__(parent)

        self.tree_widget = FilterableTreeView()
        self.add_component(self.tree_widget)
