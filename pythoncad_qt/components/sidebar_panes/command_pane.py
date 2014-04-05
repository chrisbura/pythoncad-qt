from PyQt4 import QtGui, QtCore

from ..buttons import Button
from ..base import VerticalLayout, ComponentBase
from .sidebar_pane import SidebarPane


class CenteredLabel(QtGui.QLabel):
    pass


class CenteredButton(Button):
    def __init__(self, *args, **kwargs):
        super(CenteredButton, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)


class CategoryHeading(QtGui.QLabel):
    pass


class CommandButton(QtGui.QPushButton):
    def __init__(self, icon, text, parent=None):
        super(CommandButton, self).__init__(icon, text, parent)
        self.setIconSize(QtCore.QSize(24, 24))


class Section(VerticalLayout, ComponentBase):

    title = 'Untitled'

    def __init__(self, *args, **kwargs):
        super(Section, self).__init__(*args, **kwargs)

        self.commands = []

    def setup_ui(self):
        self.label = QtGui.QLabel(self.title)
        self.add_component(self.label)

        for command in self.commands:
            command_button = CommandButton(command[0], command[1])
            self.add_component(command_button)

    def add_command(self, command):
        self.commands.append(command)


class FavoriteSection(Section):
    title = 'Favorites'

    def __init__(self, *args, **kwargs):
        super(FavoriteSection, self).__init__(*args, **kwargs)


class DrawingSection(Section):
    title = 'Drawing'

    def __init__(self, *args, **kwargs):
        super(DrawingSection, self).__init__(*args, **kwargs)
        self.add_command((QtGui.QIcon('images/new.png'), 'Point'))
        self.add_command((QtGui.QIcon('images/segment.png'), 'Segment'))
        self.add_command((QtGui.QIcon('images/circle.png'), 'Circle'))
        self.add_command((QtGui.QIcon('images/arc.png'), 'Arc'))
        self.add_command((QtGui.QIcon('images/ellipse.png'), 'Ellipse'))
        self.add_command((QtGui.QIcon('images/polygon.png'), 'Polygon'))
        self.add_command((QtGui.QIcon('images/polyline.png'), 'Polyline'))
        self.add_command((QtGui.QIcon('images/rectangle.png'), 'Rectangle'))
        self.setup_ui()


class LayerSection(Section):
    title = 'Layers'

    def __init__(self, *args, **kwargs):
        super(LayerSection, self).__init__(*args, **kwargs)
        self.add_command((QtGui.QIcon('images/new.png'), 'Create new layer'))
        self.add_command((QtGui.QIcon('images/new.png'), 'Rename existing layer'))
        self.add_command((QtGui.QIcon('images/new.png'), 'Delete existing layer'))
        self.add_command((QtGui.QIcon('images/new.png'), 'Open layer manager'))
        self.setup_ui()


class SectionContainer(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(SectionContainer, self).__init__(*args, **kwargs)

        self.favorite_section = FavoriteSection()
        self.add_component(self.favorite_section)

        self.drawing_section = DrawingSection()
        self.add_component(self.drawing_section)

        self.layer_section = LayerSection()
        self.add_component(self.layer_section)

        self.drawing_section = DrawingSection()
        self.add_component(self.drawing_section)

        self.add_stretch()


class CommandScrollArea(QtGui.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(CommandScrollArea, self).__init__(*args, **kwargs)

        self.setWidgetResizable(True)
        self.section_container = SectionContainer()
        self.setWidget(self.section_container)


class CommandListContainer(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(CommandListContainer, self).__init__(*args, **kwargs)

        # Frame is needed to solve border issue on QScrollArea (overlap when
        # horizontal bar is not visible)
        self.frame = QtGui.QFrame(self)
        self.frame_layout = QtGui.QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = CommandScrollArea(self.frame)
        self.frame_layout.addWidget(self.scroll_area)

        self.add_component(self.frame)


class CommandPane(SidebarPane):
    def __init__(self, parent=None):
        super(CommandPane, self).__init__(parent)

        self.favorites_heading = CategoryHeading('Favorites')
        self.add_component(self.favorites_heading)
        self.add_component(CenteredLabel('No favorites selected.'))
        self.add_component(CenteredButton('Manage Favorites'), alignment=QtCore.Qt.AlignCenter)

        self.all_commands_heading = CategoryHeading('Command List')
        self.add_component(self.all_commands_heading)
        self.command_list = CommandListContainer()
        self.add_component(self.command_list)
