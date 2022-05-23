import socket
import threading
import time

from chatterRoom1 import chatterRoomWindow1
from chatterRoom2 import chatterRoomWindow2
from chatterRoom3 import chatterRoomWindow3
from chatterRoom4 import chatterRoomWindow4
from chatterRoom5 import chatterRoomWindow5

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_waitingRoom = uic.loadUiType("waitingRoom.ui")[0]

class waitingRoomWindow(QDialog,QWidget,form_waitingRoom):
    ip = 'localhost'
    port = 9999
    # 대기실 포트

    def __init__(self, id):
        super(waitingRoomWindow, self).__init__()
        self.chatterRoom1 = None
        self.chatterRoom2 = None
        self.chatterRoom3 = None
        self.chatterRoom4 = None
        self.chatterRoom5 = None
        self.conn_socket = None  # 서버와 연결된 소켓
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
        speaker = self.lbName.text()
        speaker = speaker.encode(encoding="UTF-8")
        self.conn_socket.sendall(speaker)

    def recvMsg(self):  # 서버쪽에서 보낸 정보를 출력
        while True:
            try:
                msg = self.conn_socket.recv(1024).decode()
                # 대기실 접속자 정보 출력
                if msg.find("Client_Count") != -1:
                    waitmembers = msg.split("\n")
                    self.waitMembers.clear()
                    for member in range(1, len(waitmembers)):
                        self.waitMembers.addItem(waitmembers[member])
                    self.waitmemberCount.setText(str(len(waitmembers) - 1))
                # 각 채팅방의 인원수 정보를 수령하여 표현
                elif msg.find("ch_1") != -1:
                    room_info = msg.split(" ")
                    for i in room_info:
                        if i.find("ch_1") != -1:
                            roomNumber = i.find("ch_1")
                            volume = i[roomNumber+5:roomNumber+6]
                            self.chat1Volume.setText("("+volume+"/5)")
                        elif i.find("ch_2") != -1:
                            roomNumber = i.find("ch_2")
                            volume = i[roomNumber+5:roomNumber+6]
                            self.chat2Volume.setText("("+volume+"/5)")
                        elif i.find("ch_3") != -1:
                            roomNumber = i.find("ch_3")
                            volume = i[roomNumber+5:roomNumber+6]
                            self.chat3Volume.setText("("+volume+"/5)")
                        elif i.find("ch_4") != -1:
                            roomNumber = i.find("ch_4")
                            volume = i[roomNumber+5:roomNumber+6]
                            self.chat4Volume.setText("("+volume+"/5)")
                        elif i.find("ch_5") != -1:
                            roomNumber = i.find("ch_5")
                            volume = i[roomNumber+5:roomNumber+6]
                            self.chat5Volume.setText("("+volume+"/5)")
                elif msg.find("/overlap") != -1:
                    QMessageBox.about(self,"계정중복","중복된 이름으로 접속을 시도하여 종료합니다.")
                    self.close()
                    self.terminate()
            except Exception as e:
                # 오류 발생시 오류 메시지 출력후 재연결 시도
                print(e)
                self.conn()

    def enterRoom(self):               # 선택한 항목을 토대로 해당 채팅방으로 이동
        id = self.lbName.text()
        self.close()
        select = self.chatRoomList.currentRow()
        if select == 0:
            self.selectRoom(select)
            self.chatterRoom1 = chatterRoomWindow1(id)
            self.chatterRoom1.exec_()
            self.show()
        elif select == 1:
            self.selectRoom(select)
            self.chatterRoom2 = chatterRoomWindow2(id)
            self.chatterRoom2.exec_()
            self.show()
        elif select == 2:
            self.selectRoom(select)
            self.chatterRoom3 = chatterRoomWindow3(id)
            self.chatterRoom3.exec_()
            self.show()
        elif select == 3:
            self.selectRoom(select)
            self.chatterRoom4 = chatterRoomWindow4(id)
            self.chatterRoom4.exec_()
            self.show()
        elif select == 4:
            self.selectRoom(select)
            self.chatterRoom5 = chatterRoomWindow5(id)
            self.chatterRoom5.exec_()
            self.show()

    # 채팅방이 진입 가능한지 체크 (미구현)
    # def checkEnable(self,select):
    #     judge = 0
    #     current = 0
    #     if select == 0:
    #         current = self.chat1Volume().text[1]
    #     elif select == 1:
    #         current = self.chat2Volume().text[1]
    #     elif select == 2:
    #         current = self.chat3Volume().text[1]
    #     elif select == 3:
    #         current = self.chat4Volume().text[1]
    #     elif select == 4:
    #         current = self.chat5Volume().text[1]
    #
    #     if current == 5:
    #         judge = 1
    #
    #     return judge

    def selectRoom(self,msg):       # 채팅방 선택정보 전달
        result = str(msg).encode(encoding="UTF-8")
        self.conn_socket.sendall(result)

    def exit(self):                 # 로그오프
        msg = "/exit"
        exit_msg = msg.encode(encoding="UTF-8")
        self.conn_socket.sendall(exit_msg)
        self.close()
        self.terminate()

