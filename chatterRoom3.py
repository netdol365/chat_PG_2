import threading
import socket
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_chatterRoom = uic.loadUiType("chatterRoom.ui")[0]


class chatterRoomWindow3(QDialog, QWidget, form_chatterRoom):
    ip = 'localhost'
    port = 3333
    # 채팅방1
    wait_port = 9999

    # 대기실

    def __init__(self, id):
        super(chatterRoomWindow3, self).__init__()

        self.conn_socket = None  # 채팅서버와 연결된 소켓
        self.conn_socket2 = None  # 대기실서버와 연결된 소켓
        self.conn()
        self.client = None
        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.initUi(id)
        self.show()
        self.setFixedSize(644, 578)
        self.setId()

    def initUi(self, id):
        self.setupUi(self)
        self.lbName.setText(id)
        self.btnInput.clicked.connect(self.sendMsg)
        self.btnExit.clicked.connect(self.exit)
        self.setWindowTitle("채팅방1")

    def conn(self):
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_socket.connect((chatterRoomWindow3.ip, chatterRoomWindow3.port))
        self.conn_socket2.connect((chatterRoomWindow3.ip, chatterRoomWindow3.wait_port))

    def setId(self):  # 로드시 메시지를 보내 계정명을 지정
        speaker = self.lbName.text()
        speaker = speaker.encode(encoding="UTF-8")
        self.conn_socket.sendall(speaker)

    def sendMsg(self):
        msg = self.txtInput.toPlainText()
        msg = msg.encode(encoding="UTF-8")
        self.conn_socket.sendall(msg)
        # 메시지 입력 후 초기화 작업
        self.txtInput.clear()

    def recvMsg(self):  # 상대방 or 서버에서 보낸 메시지 읽어서 화면에 출력
        while True:
            try:
                msg = self.conn_socket.recv(1024).decode()
                # 채팅방 접속자 정보 출력
                if msg.find('Client_Count') != -1:
                    members = msg.split("\n")
                    print(members)
                    self.members.clear()
                    for member in range(1, len(members)):
                        print(members[member])
                        self.members.addItem(members[member])
                    self.memberCount.setText(str(len(members) - 1))
                else:
                    self.allChat.append(msg)
            except Exception as e:
                # 오류 발생시 오류 메시지 출력후 재연결 시도
                print(e)
                self.conn()
                pass

    def exit(self):  # 채팅방 나가는 기능
        msg = "/exit"
        msg2 = "/home:3"
        speaker = self.lbName.text()
        speaker = speaker.encode(encoding="UTF-8")
        exit_msg = msg.encode(encoding="UTF-8")
        home_msg = msg2.encode(encoding="UTF-8")
        self.conn_socket.sendall(exit_msg)
        self.conn_socket2.sendall(speaker)
        time.sleep(0.5)
        self.conn_socket2.sendall(home_msg)
        self.close()

# --------------------------------------------------------------------------------------------------
# 서버 오류시 경고창 실행(미필요)
# def warningEvent(self):
#     reply = QMessageBox.warning(self, "오류 발생", "채팅방 서버에 오류가 발생하여 이용할 수 없습니다.",
#                                 QMessageBox.Yes, QMessageBox.Yes)
#     if reply == QMessageBox.Yes:
#         self.close()