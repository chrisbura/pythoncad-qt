
from PyQt4 import QtCore, QtGui

from components.base import ComponentBase, VerticalLayout
from components.document import Document


class DocumentControl(VerticalLayout, ComponentBase):

    def __init__(self, *args, **kwargs):
        super(DocumentControl, self).__init__(*args, **kwargs)

        self.document = Document()
        self.add_component(self.document)
