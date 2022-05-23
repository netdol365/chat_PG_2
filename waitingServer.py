import socket, threading
import time


class waitingRoom:  # 채팅방 클래스.
    def __init__(self):
        self.waitclients = []       # 대기자 명단을 보관
        self.chat_1 = []            # 각 채팅방별 명단 보관
        self.chat_2 = []
        self.chat_3 = []
        self.chat_4 = []
        self.chat_5 = []

    def addClient(self, client):  # 클라이언트 리스트 추가 후 스레드에 지정
        self.waitclients.append(client)

    def delClient(self, client):
        self.waitclients.remove(client)

    def showClients(self):        # 대기자 명단 반영 ( 대기자 명단이 없으면 반복 이탈 )
        result = "Client_Count"
        for client in self.waitclients:
            if client.id is None:
                continue
            result += "\n" + str(client.id)
        return result

    def showWaitingUser(self):
        result = []
        for client in self.waitclients:
            result.append(client.id)
        return result

    def sendMsgAll(self, msg):  # 대기방에 있는 모든 유저에게 대기방 정보 반영
        for client in self.waitclients:
            client.sendMsg(msg)

    def addChat(self,client,room):  # 채팅방 입장 유저 및 유저 인원수 추가
        if room == "0":
            self.chat_1.append(client)
        elif room == "1":
            self.chat_2.append(client)
        elif room == "2":
            self.chat_3.append(client)
        elif room == "3":
            self.chat_4.append(client)
        else:
            self.chat_5.append(client)

    def delChat(self,client,room):  # 채팅방 퇴장 유저 및 유저 인원수 감소
        if room == "1":
            self.chat_1.remove(client)
        elif room == "2":
            self.chat_2.remove(client)
        elif room == "3":
            self.chat_3.remove(client)
        elif room == "4":
            self.chat_4.remove(client)
        else:
            self.chat_5.remove(client)

    def showChatroomVolume(self):         # 채팅방 인원수 반영
        result = "ch_1:" + str(len(self.chat_1))+" "
        result += "ch_2:" + str(len(self.chat_2))+" "
        result += "ch_3:" + str(len(self.chat_3))+" "
        result += "ch_4:" + str(len(self.chat_4))+" "
        result += "ch_5:" + str(len(self.chat_5))
        return result

class waitClient:

    def __init__(self, room, socket):
        self.room = room  # 대기방. waitingRoom 객체
        self.id = None  # 사용자 id
        self.fruits = None
        self.socket = socket  # 사용자와 1:1 통신할 소켓

    def readMsg(self):
        self.id = self.socket.recv(1024).decode()

        # 접속 유저 이름 중복 여부 확인
        clients = self.room.showWaitingUser()
        if clients.count(self.id) > 1:
            self.sendMsg('/overlap')
            self.room.delClient(self)

        self.room.sendMsgAll(self.room.showClients())  # 대기 유저 목록
        self.room.sendMsgAll(self.room.showChatroomVolume())  # 채팅방 별 유저 목록

        # 대기실 정보 갱신
        while True:
            try:
                msg = self.socket.recv(1024).decode()
                self.room.sendMsgAll(self.room.showClients())
                if msg == '/exit':  # 로그아웃
                    self.room.delClient(self)
                    self.room.sendMsgAll(self.room.showClients())
                    print("퇴장")
                elif msg.find("/home") != -1:
                    msg = msg.split(":")[1]
                    print(msg)
                    self.room.addClient(self)
                    self.room.delChat(self.id,msg)
                    self.room.sendMsgAll(self.room.showClients())
                    time.sleep(0.5)
                    self.room.sendMsgAll(self.room.showChatroomVolume())
                else:  # 채팅방으로 진입
                    self.room.addChat(self.id, msg)
                    print(self.room.waitclients)
                    self.room.delClient(self)
                    self.room.sendMsgAll(self.room.showClients())
                    time.sleep(0.5)
                    self.room.sendMsgAll(self.room.showChatroomVolume())
                    print("채팅방에 진입")
            except Exception as e:
                print(e)
                waitingserver = waitingServer()
                waitingserver.run()

    def sendMsg(self, msg):
        self.socket.sendall(msg.encode(encoding='utf-8'))

class waitingServer:
    ip = 'localhost'  # or 본인 ip or 127.0.0.1
    port = 9999
    # 대기실 포트

    def __init__(self):
        self.server_socket = None  # 서버 소켓(대문)
        self.room = waitingRoom()

    def open(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((waitingServer.ip, waitingServer.port))
        self.server_socket.listen()

    def run(self):
        self.open()
        print('waitingServer is Running...')

        while True:
            client_socket, addr = self.server_socket.accept()
            print(addr, '접속')
            client = waitClient(self.room, client_socket)
            self.room.addClient(client)
            th = threading.Thread(target=client.readMsg)
            th.start()
            
            # 서버 유지를 위한 삭제
            # if threading.active_count() == 0:
            #     break

def main():
    waitingserver = waitingServer()
    waitingserver.run()

main()