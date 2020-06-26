import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from win32api import LoadKeyboardLayout

# set russian as default layout
LoadKeyboardLayout("00000419", 1)

# directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 750)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.load_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_file_button.setGeometry(QtCore.QRect(40, 20, 130, 30))
        self.load_file_button.setFont(font)
        self.load_file_button.setObjectName("load_file_button")
        self.load_file_button.clicked.connect(self.load_file)

        self.save_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_file_button.setGeometry(QtCore.QRect(720, 20, 130, 30))
        self.save_file_button.setFont(font)
        self.save_file_button.setObjectName("save_file_button")
        self.save_file_button.clicked.connect(self.save_file)
        self.my_file_name = ''

        self.image_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.image_text.setGeometry(QtCore.QRect(70, 410, 761, 121))
        self.image_text.setFont(font)
        self.image_text.setObjectName("image_text")
        self.file_name = QtWidgets.QLabel(self.centralwidget)
        self.file_name.setGeometry(QtCore.QRect(340, 350, 201, 31))
        self.file_name.setFont(font)
        self.file_name.setAutoFillBackground(False)
        self.file_name.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name.setObjectName("file_name")
        self.who_answer = QtWidgets.QLineEdit(self.centralwidget)
        self.who_answer.setGeometry(QtCore.QRect(280, 560, 140, 20))
        self.who_answer.setFont(font)
        self.who_answer.setMaxLength(100)
        self.who_answer.setObjectName("who_answer")
        self.who_question = QtWidgets.QLineEdit(self.centralwidget)
        self.who_question.setGeometry(QtCore.QRect(70, 560, 190, 20))
        self.who_question.setFont(font)
        self.who_question.setMaxLength(100)
        self.who_question.setObjectName("who_question")
        self.verb_question = QtWidgets.QLineEdit(self.centralwidget)
        self.verb_question.setGeometry(QtCore.QRect(70, 600, 190, 20))
        self.verb_question.setFont(font)
        self.verb_question.setMaxLength(100)
        self.verb_question.setObjectName("verb_question")
        self.hand_question = QtWidgets.QLineEdit(self.centralwidget)
        self.hand_question.setGeometry(QtCore.QRect(70, 640, 190, 20))
        self.hand_question.setFont(font)
        self.hand_question.setMaxLength(100)
        self.hand_question.setObjectName("hand_question")
        self.location_quesion = QtWidgets.QLineEdit(self.centralwidget)
        self.location_quesion.setGeometry(QtCore.QRect(70, 680, 190, 20))
        self.location_quesion.setFont(font)
        self.location_quesion.setMaxLength(100)
        self.location_quesion.setObjectName("location_question")
        self.verb_answer = QtWidgets.QLineEdit(self.centralwidget)
        self.verb_answer.setGeometry(QtCore.QRect(280, 600, 140, 20))
        self.verb_answer.setFont(font)
        self.verb_answer.setMaxLength(100)
        self.verb_answer.setObjectName("verb_answer")
        self.hand_answer = QtWidgets.QLineEdit(self.centralwidget)
        self.hand_answer.setGeometry(QtCore.QRect(280, 640, 140, 20))
        self.hand_answer.setFont(font)
        self.hand_answer.setMaxLength(100)
        self.hand_answer.setObjectName("hand_answer")
        self.location_answer = QtWidgets.QLineEdit(self.centralwidget)
        self.location_answer.setGeometry(QtCore.QRect(280, 680, 140, 20))
        self.location_answer.setFont(font)
        self.location_answer.setMaxLength(100)
        self.location_answer.setObjectName("location_answer")
        self.own_answer_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_answer_4.setGeometry(QtCore.QRect(690, 680, 140, 20))
        self.own_answer_4.setFont(font)
        self.own_answer_4.setMaxLength(100)
        self.own_answer_4.setObjectName("own_answer_4")
        self.own_answer_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_answer_3.setGeometry(QtCore.QRect(690, 640, 140, 20))
        self.own_answer_3.setFont(font)
        self.own_answer_3.setMaxLength(100)
        self.own_answer_3.setObjectName("own_answer_3")
        self.own_question_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_question_1.setGeometry(QtCore.QRect(480, 560, 190, 20))
        self.own_question_1.setFont(font)
        self.own_question_1.setText("")
        self.own_question_1.setMaxLength(100)
        self.own_question_1.setObjectName("own_question_1")
        self.own_question_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_question_2.setGeometry(QtCore.QRect(480, 600, 190, 20))
        self.own_question_2.setFont(font)
        self.own_question_2.setText("")
        self.own_question_2.setMaxLength(100)
        self.own_question_2.setObjectName("own_question_2")
        self.own_answer_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_answer_1.setGeometry(QtCore.QRect(690, 560, 140, 20))
        self.own_answer_1.setFont(font)
        self.own_answer_1.setMaxLength(100)
        self.own_answer_1.setObjectName("own_answer_1")
        self.own_question_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_question_3.setGeometry(QtCore.QRect(480, 640, 190, 20))
        self.own_question_3.setFont(font)
        self.own_question_3.setText("")
        self.own_question_3.setMaxLength(100)
        self.own_question_3.setObjectName("own_question_3")
        self.own_question_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_question_4.setGeometry(QtCore.QRect(480, 680, 190, 20))
        self.own_question_4.setFont(font)
        self.own_question_4.setText("")
        self.own_question_4.setMaxLength(100)
        self.own_question_4.setObjectName("own_question_4")
        self.own_answer_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.own_answer_2.setGeometry(QtCore.QRect(690, 600, 140, 20))
        self.own_answer_2.setFont(font)
        self.own_answer_2.setMaxLength(100)
        self.own_answer_2.setObjectName("own_answer_2")
        self.loaded_image = QtWidgets.QLabel(self.centralwidget)
        self.loaded_image.setGeometry(QtCore.QRect(220, 20, 450, 300))
        self.loaded_image.setAutoFillBackground(True)
        self.loaded_image.setFrameShape(QtWidgets.QFrame.Box)
        self.loaded_image.setAlignment(QtCore.Qt.AlignCenter)
        self.loaded_image.setObjectName("loaded_image")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 540, 50, 15))
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(550, 540, 50, 15))
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(320, 540, 50, 15))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(730, 540, 50, 15))
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.faq_list = ((self.who_question, self.who_answer),
                         (self.verb_question, self.verb_answer),
                         (self.hand_question, self.hand_answer),
                         (self.location_quesion, self.location_answer),
                         (self.own_question_1, self.own_answer_1),
                         (self.own_question_2, self.own_answer_2),
                         (self.own_question_3, self.own_answer_3),
                         (self.own_question_4, self.own_answer_4)
                         )

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_file_button.setText(_translate("MainWindow", "Load image"))
        self.save_file_button.setText(_translate("MainWindow", "Save CSV"))
        self.image_text.setPlaceholderText(
            _translate("MainWindow", "Описание картинки"))
        self.file_name.setText(
            _translate("MainWindow", "Lable to show file name"))
        self.who_answer.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.who_question.setText(_translate("MainWindow", "Кто на картинке?"))
        self.who_question.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.verb_question.setText(_translate("MainWindow", "Что делает?"))
        self.verb_question.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.hand_question.setText(_translate("MainWindow", "Что в руках?"))
        self.hand_question.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.location_quesion.setText(
            _translate("MainWindow", "Где находится?"))
        self.location_quesion.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.verb_answer.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.hand_answer.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.location_answer.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.own_answer_4.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.own_answer_3.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.own_question_1.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.own_question_2.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.own_answer_1.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.own_question_3.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.own_question_4.setPlaceholderText(
            _translate("MainWindow", "Введите вопрос"))
        self.own_answer_2.setPlaceholderText(
            _translate("MainWindow", "Введите ответ"))
        self.loaded_image.setText(_translate("MainWindow", "Image to show"))
        self.label_2.setText(_translate("MainWindow", "Вопрос"))
        self.label_3.setText(_translate("MainWindow", "Вопрос"))
        self.label_4.setText(_translate("MainWindow", "Ответ"))
        self.label_5.setText(_translate("MainWindow", "Ответ"))

    def load_file(self):
        name, filters = QtWidgets.QFileDialog.getOpenFileName(
            caption='Открыть файл', directory='./img',
            filter="Image files (*.jpg *.jpeg *.png)")
        print(name)
        self.my_file_name = name.split('/')[-1]
        print(self.my_file_name)
        self.loaded_image.setPixmap(QtGui.QPixmap(name).scaledToWidth(450))
        self.file_name.setText(self.my_file_name)
        print('Clicked')

    def form_checker(self):
        pass

    def save_file(self):
        self.form_checker()
        with open('./data/output.csv', 'a', encoding='utf-8') as outFile:
            print(','.join(self.generate_line()), file=outFile)

    #            print(','.join(self.generate_line()))
    #            self.generate_line()
    '''
            name, filters = QtWidgets.QFileDialog.getSaveFileName(
                caption='Save File', directory='.\data')
            print(name)
    '''

    def generate_line(self):
        generated_line = [self.my_file_name, self.image_text.toPlainText()]
        for item in self.faq_list:
            question, answer = item
            if question.text() == '' or answer.text() == '':
                continue
            generated_line.append(question.text())
            generated_line.append(answer.text())
        return generated_line


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
# print(ui.generate_line())
sys.exit(app.exec_())
