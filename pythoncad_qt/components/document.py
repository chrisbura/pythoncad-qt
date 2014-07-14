from PyQt4 import QtCore, QtGui


from components.base import ComponentBase, VerticalLayout, HorizontalLayout
from components.buttons import Button, ToggleButton
from components.view.document_view import DocumentView
from components.view.document_scene import DocumentScene
from dialogs.document_properties import DocumentPropertiesDialog
import settings

class DocumentTitleLabel(QtGui.QLabel):
    pass


class TitleBar(HorizontalLayout, ComponentBase):

    layout_margins = QtCore.QMargins(0, 0, 11, 0)
    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        # TODO: Double click to edit title
        self.title = DocumentTitleLabel()
        self.filename = QtGui.QLabel()

        self.add_component(self.title)
        self.add_component(self.filename)
        self.add_component(Button('Save'))
        self.add_component(Button('Save As'))
        self.add_component(Button('Properties',
            clicked=self.open_document_properties_dialog))
        self.add_component(Button('Close'))

        self.add_stretch()

        self.expand = Button(QtGui.QIcon('images/maximize.png'), 'Expand')
        self.add_component(self.expand)

    def set_filename(self, filename):
        self.filename.setText(filename)

    def set_title(self, title):
        self.title.setText(title)

    def open_document_properties_dialog(self):
        document_properties_dialog = DocumentPropertiesDialog(
            drawing=self.drawing, parent=self)
        dialog_return = document_properties_dialog.exec_()

        if dialog_return == QtGui.QDialog.Accepted:
            # TODO: Error checking
            # TODO: Auto update title using signal
            drawing_title = str(document_properties_dialog.form.fields['title'].text())
            self.drawing.set_title(drawing_title)
            self.set_title(drawing_title)
        else:
            # TODO: Reset fields
            print 'Rejected'



class SceneCoordinates(QtGui.QLabel):
    pass


class GraphicsStatusBar(HorizontalLayout, ComponentBase):

    layout_margins = QtCore.QMargins(5, 5, 5, 5)
    layout_spacing = 6

    def __init__(self, *args, **kwargs):
        super(GraphicsStatusBar, self).__init__(*args, **kwargs)

        # Snap Toggle
        # TODO: Wire it up
        self.snap_toggle = ToggleButton(QtGui.QIcon('images/SSnap.png'), 'Snap')
        self.add_component(self.snap_toggle)

        # Grid Toggle
        self.grid_toggle = ToggleButton(QtGui.QIcon('images/SGrid.png'), 'Grid')
        if settings.DRAW_GRID:
            self.grid_toggle.setChecked(True)
        self.add_component(self.grid_toggle)

        # Axes Toggle
        self.axes_toggle = ToggleButton(QtGui.QIcon('images/SGrid.png'), 'Axes')
        if settings.DRAW_AXES:
            self.axes_toggle.setChecked(True)
        self.add_component(self.axes_toggle)

        self.snap_auto = ToggleButton(QtGui.QIcon('images/snapauto.png'), '')
        self.add_component(self.snap_auto)

        self.snap_endpoint = ToggleButton(QtGui.QIcon('images/snapend.png'), '')
        self.add_component(self.snap_endpoint)

        self.snap_centerpoint = ToggleButton(QtGui.QIcon('images/snapcen.png'), '')
        self.add_component(self.snap_centerpoint)

        self.snap_midpoint = ToggleButton(QtGui.QIcon('images/snapmid.png'), '')
        self.add_component(self.snap_midpoint)

        self.snap_quarter = ToggleButton(QtGui.QIcon('images/snapqua.png'), '')
        self.add_component(self.snap_quarter)

        self.add_stretch()

        self.scene_coordinates = SceneCoordinates('X: 0.000 Y: 0.000')
        self.add_component(self.scene_coordinates)

    def update_coordinates(self, x, y):
        self.scene_coordinates.setText('X: {0} Y: {1}'.format(x, y))

    def reset_coordinates(self, event):
        self.scene_coordinates.setText('X: ----- Y: -----')


class Document(VerticalLayout, ComponentBase):
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

        self.titlebar = TitleBar()

        self.scene = DocumentScene(parent=self)
        self.view = DocumentView(self.scene, parent=self)

        self.status_bar = GraphicsStatusBar()
        self.status_bar.grid_toggle.toggled.connect(self.scene.toggle_grid)
        self.status_bar.axes_toggle.toggled.connect(self.scene.toggle_axes)

        # Signals
        self.scene.mouse_move.connect(self.status_bar.update_coordinates)
        self.view.mouse_exit.connect(self.status_bar.reset_coordinates)

        self.add_component(self.titlebar)
        self.add_component(self.view)
        self.add_component(self.status_bar)

    def load_drawing(self, drawing):
        # self.scene.reset_scene()
        self.titlebar.set_title(drawing.title)
