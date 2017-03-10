from PyQt5 import QtWidgets


class ProgressBar(QtWidgets.QProgressBar):
    value = 0

    def increase_value(self):
        self.setValue(self.value)
        self.value += 1

    def set_value(self, value):
        self.setValue(value)
        self.value = value
