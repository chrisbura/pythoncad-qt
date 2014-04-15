from PyQt4 import QtGui, QtCore

from components.buttons import PrimaryButton, WarningButton
from components.base import ComponentBase, VerticalLayout
from components.constants import MARGINS_ZERO


class FieldLayout(VerticalLayout, ComponentBase):
    layout_spacing = 6


class FormBase(VerticalLayout, ComponentBase):
    layout_spacing = 12
    layout_margins = QtCore.QMargins(0, 10, 0, 10)

    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)
        self.fields = {}

    def add_field(self, title, field_widget):
        # TODO: Add validators
        # TODO: Error checking

        # Field Layout
        field_layout = FieldLayout()
        label = QtGui.QLabel(title.capitalize())
        field_layout.add_component(label)

        self.fields[title] = field_widget
        field_layout.add_component(self.fields[title])

        self.add_component(field_layout)

class DocumentPropertiesForm(FormBase):

    def __init__(self, drawing, *args, **kwargs):
        super(DocumentPropertiesForm, self).__init__(*args, **kwargs)

        self.drawing = drawing

        # Fields
        self.add_field('title', QtGui.QLineEdit(self.drawing.get_property('drawing_title').value))
        self.add_stretch()


class DialogLabel(QtGui.QLabel):
    pass


class DocumentPropertiesDialog(QtGui.QDialog):
    def __init__(self, drawing, *args, **kwargs):
        super(DocumentPropertiesDialog, self).__init__(*args, **kwargs)

        self.drawing = drawing

        self.setWindowTitle('Document Properties')

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        # Dialog Label
        # TODO: Use group box
        self.dialog_label = DialogLabel('Document Properties')
        self.layout.addWidget(self.dialog_label)

        # Form
        self.form = DocumentPropertiesForm(drawing=self.drawing)
        self.layout.addWidget(self.form)

        # Buttons
        self.ok_button = PrimaryButton('Save', clicked=self.accept)
        self.cancel_button = WarningButton('Cancel', clicked=self.reject)

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)
