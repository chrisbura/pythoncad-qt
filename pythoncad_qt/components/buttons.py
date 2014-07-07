from PyQt4 import QtGui


class Button(QtGui.QPushButton):
    pass


class PrimaryButton(Button):
    pass


class DangerButton(Button):
    pass


class WarningButton(Button):
    pass


class ToggleButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(ToggleButton, self).__init__(*args, **kwargs)
        self.setCheckable(True)
