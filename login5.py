import sys

from waitingRoom import waitingRoomWindow
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_login = uic.loadUiType("login.ui")[0]

class LoginWindow(QMainWindow, form_login):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.initUI()
        self.show()
        self.id = None
        self.setFixedSize(463, 296)

    # 계정 생성창
    def initUI(self):
        self.setupUi(self)
        # Enter 인식
        self.txtName.returnPressed.connect(self.goWaitingRoom)
        self.btnInput.clicked.connect(self.goWaitingRoom)

    # 대기방 이동 기능
    def goWaitingRoom(self):
        id = self.txtName.text()

        if id.isspace():
            QMessageBox.about(self,"부적절한계정","공백을 사용할 수 없습니다.")
            return 0
        else:
            self.close()
            self.waitingRoom = waitingRoomWindow(id)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    loginWindow.show()
    sys.exit(app.exec())