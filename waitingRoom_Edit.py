import socket
import threading
import time

from chatterRoom_Edit import chatterRoomWindow
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_waitingRoom = uic.loadUiType("waitingRoom.ui")[0]

class waitingRoomWindow(QDialog,QWidget,form_waitingRoom):
    ip = 'localhost'
    port = 9999
    def __init__(self, id):
        super(waitingRoomWindow, self).__init__()
        self.conn_socket = None
        self.chatterRoom = None
        self.conn()
        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.initUi(id)
        self.show()
        self.setFixedSize(458, 531)
        self.setId()


    def initUi(self,id):
        self.setupUi(self)
        self.chatRoomList.itemDoubleClicked.connect(self.enterRoom)
        self.btnQuit.clicked.connect(self.exit)
        self.btnGetin.clicked.connect(self.enterRoom)
        self.lbName.setText(id)

    def conn(self):
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_socket.connect((waitingRoomWindow.ip, waitingRoomWindow.port))

    def setId(self): # 로드시 메시지를 보내 계정명을 지정
        speaker = self.lbName.text()             # 0 ==> 대기실
        speaker = speaker.encode(encoding="UTF-8")
        self.conn_socket.sendall(speaker)

    def recvMsg(self):  # 서버쪽에서 보낸 정보를 출력
        while True:
            try:
                msg = self.conn_socket.recv(1024).decode()
                # 대기실 접속자 정보 출력
                if msg.startswith("Client_List"):
                    waitmembers = msg.split("\n")
                    self.waitMembers.clear()
                    for member in range(1, len(waitmembers)):
                        self.waitMembers.addItem(waitmembers[member])
                    self.waitmemberCount.setText(str(len(waitmembers) - 1))
                # 각 채팅방의 인원수 정보를 수령하여 표현
                elif msg.startswith("Client_Count"):
                    msg = msg.split(":")
                    ch1 = "(" + msg[2] + "/5)"
                    ch2 = "(" + msg[4] + "/5)"
                    ch3 = "(" + msg[6] + "/5)"
                    ch4 = "(" + msg[8] + "/5)"
                    ch5 = "(" + msg[10] + "/5)"
                    self.chat1Volume.setText(ch1)
                    self.chat2Volume.setText(ch2)
                    self.chat3Volume.setText(ch3)
                    self.chat4Volume.setText(ch4)
                    self.chat5Volume.setText(ch5)
                elif msg.find("/overlap") != -1:
                    QMessageBox.about(self,"계정중복","중복된 이름으로 접속을 시도하여 종료합니다.")
                    self.exit()
            except Exception as e:
                # 오류 발생시 오류 메시지 출력후 재연결 시도
                print(e)
                self.conn()

    def enterRoom(self):               # 선택한 항목을 토대로 해당 채팅방으로 이동
        id = self.lbName.text()
        select = self.chatRoomList.currentRow()

        # if self.checkEnable(select) == 1:
        #     QMessageBox.about(self, "정원초과", "채팅방의 정원이 제한되어 입장할 수 없습니다.")
        #     return 0
        if select == 0:
            self.selectRoom(select)
        elif select == 1:
            self.selectRoom(select)
        elif select == 2:
            self.selectRoom(select)
        elif select == 3:
            self.selectRoom(select)
        elif select == 4:
            self.selectRoom(select)

        self.close()
        self.chatterRoom = chatterRoomWindow(id,select)
        self.chatterRoom.exec_()
        self.show()

    # 채팅방이 진입 가능한지 체크 (미구현)
    def checkEnable(self,select):   # 1 ==> 만원
        judge = 0
        current = 0
        if select == 0:
            current = self.chat1Volume().text[1]
        elif select == 1:
            current = self.chat2Volume().text[1]
        elif select == 2:
            current = self.chat3Volume().text[1]
        elif select == 3:
            current = self.chat4Volume().text[1]
        elif select == 4:
            current = self.chat5Volume().text[1]

        if current == "5":
            judge = 1

        return judge

    def selectRoom(self,select):       # 채팅방 선택정보 전달
        select +=1                     # 인덱스 값 보정
        result = "select_room:"
        result += str(select)
        result = result.encode(encoding="UTF-8")
        self.conn_socket.sendall(result)
        time.sleep(0.5)
        self.conn_socket.close()

    def exit(self):                 # 로그오프
        msg = "/quit"
        quit_msg = msg.encode(encoding="UTF-8")
        self.conn_socket.sendall(quit_msg)
        self.close()
        time.sleep(5)
        self.conn_socket.close()
        self.terminate()

