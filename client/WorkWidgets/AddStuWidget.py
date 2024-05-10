from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from ClientSocket.SocketClient import SocketClient
from ClientCommand.AddStru import AddStru

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self, client:SocketClient):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.client = client
        self.add_stru = AddStru(self.client)
        # validator
        int_validator = QtGui.QIntValidator(0, 100)

        # label
        header_label = self.init_label_widget(20, "Add Student")
        name_label = self.init_label_widget(16, "Name:")
        subject_label = self.init_label_widget(16, "Subject:")
        score_label = self.init_label_widget(16, "Score:")
        self.info_label = self.init_label_widget(16, "")
        self.info_label.setStyleSheet("color: red;") # set text color
        # editor_label
        self.name_editor_label = LineEditComponent("Name")
        self.name_editor_label.mousePressEvent = self.clear_name_editor_content
        self.name_editor_label.textChanged.connect(self.name_editor_text_changed)
        
        self.subject_editor_label = LineEditComponent("Subject")
        self.subject_editor_label.mousePressEvent = self.clear_subject_editor_content
        self.subject_editor_label.setEnabled(False)

        self.score_editor_label = LineEditComponent("")
        self.score_editor_label.setValidator(int_validator)
        self.score_editor_label.setEnabled(False)
        
        # button
        self.query_btn = self.init_setting_btn("Query", self.query_action, False)
        self.add_btn = self.init_setting_btn("Add", self.add_action, False)
        self.send_btn = self.init_setting_btn("Send", self.send_action, True)

        layout = QtWidgets.QGridLayout()
        # set label layout        
        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.info_label, 1, 3, 10, 10)
        # set editor label layout
        layout.addWidget(self.name_editor_label, 1, 1, 1, 1)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 1)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 1)
        # set button layout
        layout.addWidget(self.query_btn, 1, 2, 1, 1)
        layout.addWidget(self.add_btn, 3, 2, 1, 1)
        layout.addWidget(self.send_btn, 5, 3, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 4)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 2)

        self.setLayout(layout)
        self.score_dict = {}

    
    def clear_name_editor_content(self, event):
        self.name_editor_label.clear()

    def clear_subject_editor_content(self, event):
        self.subject_editor_label.clear()
    def init_setting_btn(self, btn_label, click_event, btn_enable : bool):
        btn = ButtonComponent(btn_label)
        btn.clicked.connect(click_event)
        btn.setEnabled(btn_enable)

        return btn
    # query btn clicked event
    def query_action(self):
        query_result = self.add_stru.query_name(self.name_editor_label.text())
        print(f"Query name: {self.name_editor_label.text()}")        
        # if status: 'Fail'
        if query_result['status'] == "Fail":
            self.info_label.setText(f"Query success")
            self.add_stru.add_name(self.name_editor_label.text())
            self.setWidgetEnable(False, True, True, False)
        else:
            print(f"The name {self.name_editor_label.text()} is already in the list.")
            self.info_label.setText(f"The name {self.name_editor_label.text()} is already in the list.")
            self.name_editor_label.setText("Name")
        
    # add btn clicked event
    def add_action(self):
        if self.subject_editor_label.text() != '' and self.subject_editor_label.text() != 'Subject' and self.score_editor_label.text() != '':
            self.add_stru.add_subject_and_score(self.subject_editor_label.text(), self.score_editor_label.text())
            self.info_label.setText(f"add {self.subject_editor_label.text()} : {self.score_editor_label.text()}")
            # print(f"score_dict: {self.score_dict}")
            self.subject_editor_label.setText('')
            self.score_editor_label.setText('')
        else:
            print("Please input subject and score.")
            self.info_label.setText("Please input subject and score.")

    # send btn clicked event
    def send_action(self):
        if self.name_editor_label.text() != "Name" and not self.query_btn.isEnabled():
            result = self.add_stru.send_parameters_to_server()
            if result['status'] == "OK":
                self.info_label.setText("Add success!")
                # reset component status
                self.add_stru.reset_parameters()
                self.setWidgetEnable(True, False, False, False)
                self.name_editor_label.setText("Name")
                self.subject_editor_label.setText("Subject")
            
    
    # widget enable setting
    def setWidgetEnable(self, name_editor_enable=True, subject_and_score_editor_enable=True, add_btn_enable=True, query_btn_enable=True):
        self.name_editor_label.setEnabled(name_editor_enable)
        self.subject_editor_label.setEnabled(subject_and_score_editor_enable)
        self.score_editor_label.setEnabled(subject_and_score_editor_enable)
        self.add_btn.setEnabled(add_btn_enable)
        self.query_btn.setEnabled(query_btn_enable)
    

    # setting label widget
    def init_label_widget(self, font_size, init_content):
        label = LabelComponent(font_size, init_content)
        label.setFont(self.label_font("Arial", font_size))

        return label
    # setting editor label widget
    def init_editor_label_widget(self, font_size, init_content):
        editor_label = LineEditComponent(init_content)
        editor_label.setFont(self.label_font("Arial", font_size))
        editor_label.mousePressEvent = self.clear_name_editor_content
        editor_label.textChanged.connect(self.name_editor_text_changed)

        return editor_label
    
    # name editor label text changed event
    def name_editor_text_changed(self, text):
        self.name_editor_label.setText(text)

        if text == 'Name' or text == '':
            self.query_btn.setEnabled(False)
        else:
            self.query_btn.setEnabled(True)
    # setting label font
    def label_font(self, word_font : str, font_size):
        content_font = QtGui.QFont()
        content_font.setFamily(word_font)
        content_font.setPointSize(font_size)

        return content_font