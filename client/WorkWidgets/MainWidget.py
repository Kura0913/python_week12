from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
from ClientSocket.SocketClient import SocketClient


class MainWidget(QtWidgets.QWidget):
    def __init__(self, client:SocketClient):
        super().__init__()
        self.setObjectName("main_widget")

        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(24, "Student Management System")
        add_stu_widget = AddStuWidget(client)

        layout.addWidget(header_label, stretch=15)
        layout.addWidget(add_stu_widget, stretch=85)

        self.setLayout(layout)
