import socket, threading

class Room:  # 채팅방, 대기방 클래스.
    def __init__(self):
        self.chatclients_1 = []
        self.chatclients_2 = []
        self.chatclients_3 = []
        self.chatclients_4 = []
        self.chatclients_5 = []
        self.waitclients = []
        

    def addClient(self, client, select):  # 클라이언트 리스트 추가 후 스레드에 지정

        if select == 0:
            self.waitclients.append(client)
        elif select == 1:
            self.chatclients_1.append(client)
        elif select == 2:
            self.chatclients_2.append(client)
        elif select == 3:
            self.chatclients_3.append(client)
        elif select == 4:
            self.chatclients_4.append(client)
        elif select == 5:
            self.chatclients_5.append(client)

    def delClient(self, client, select): # 클라이언트 리스트에서 제거후 스레드에서 제외

        if select == 0:
            self.waitclients.remove(client)
        elif select == 1:
            self.chatclients_1.remove(client)
        elif select == 2:
            self.chatclients_2.remove(client)
        elif select == 3:
            self.chatclients_3.remove(client)
        elif select == 4:
            self.chatclients_4.remove(client)
        elif select == 5:
            self.chatclients_5.remove(client)

    def sendMsgAll(self, msg, select):  # 방에 있는 모든 사람한테 메시지 전송

        if select == 0:
            for client in self.waitclients:
                client.sendMsg(msg)
        elif select == 1:
            for client in self.chatclients_1:
                client.sendMsg(msg)
        elif select == 2:
            for client in self.chatclients_2:
                client.sendMsg(msg)
        elif select == 3:
            for client in self.chatclients_3:
                client.sendMsg(msg)
        elif select == 4:
            for client in self.chatclients_4:
                client.sendMsg(msg)
        elif select == 5:
            for client in self.chatclients_5:
                client.sendMsg(msg)

    def sendMsgExcept(self, msg, select):  # 방에 있는 자신을 제외한 모든 사람한테 메시지 전송

        if select == 0:
            for client in self.waitclients:
                if msg.find(client.id) == -1:
                    client.sendMsg(msg)
        elif select == 1:
            for client in self.chatclients_1:
                if msg.find(client.id) == -1:
                    client.sendMsg(msg)
        elif select == 2:
            for client in self.chatclients_2:
                if msg.find(client.id) == -1:
                    client.sendMsg(msg)
        elif select == 3:
            for client in self.chatclients_3:
                if msg.find(client.id) == -1:
                    client.sendMsg(msg)
        elif select == 4:
            for client in self.chatclients_4:
                if msg.find(client.id) == -1:
                    client.sendMsg(msg)
        elif select == 5:
            for client in self.chatclients_5:
                if msg.find(client.id) == -1:
                    client.sendMsg(msg)

    def showClients(self, select):        # 방 접속자들 목록 출력

        result = "Client_List"
        if select == 0:
            for client in self.waitclients:
                result += "\n" + str(client.id)
        elif select == 1:
            for client in self.chatclients_1:
                result += "\n" + str(client.id)
        elif select == 2:
            for client in self.chatclients_2:
                result += "\n" + str(client.id)
        elif select == 3:
            for client in self.chatclients_3:
                result += "\n" + str(client.id)
        elif select == 4:
            for client in self.chatclients_4:
                result += "\n" + str(client.id)
        elif select == 5:
            for client in self.chatclients_5:
                result += "\n" + str(client.id)

        return result

    def summaryCount(self):     # 채팅방1=[2], 채팅방2=[4], ...2*1...

        result = "Client_Count"
        result += ":ch_1:"+str(len(self.chatclients_1))
        result += ":ch_2:"+str(len(self.chatclients_2))
        result += ":ch_3:"+str(len(self.chatclients_3))
        result += ":ch_4:"+str(len(self.chatclients_4))
        result += ":ch_5:"+str(len(self.chatclients_5))

        return result

    def checkClient(self, id, select):    # id와 일치 여부 판별

        judge = 0

        if select == 0:
            for i in self.waitclients:
                if i.id == id:
                    judge = 1
        elif select == 1:
            for i in self.chatclients_1:
                if i.id == id:
                    judge = 1
        elif select == 2:
            for i in self.chatclients_2:
                if i.id == id:
                    judge = 1
        elif select == 3:
            for i in self.chatclients_3:
                if i.id == id:
                    judge = 1
        elif select == 4:
            for i in self.chatclients_4:
                if i.id == id:
                    judge = 1
        elif select == 5:
            for i in self.chatclients_5:
                if i.id == id:
                    judge = 1

        return judge

    def setWhipser(self, id, select):       # 귓속말 상대 설정

        result = ""

        if select == 0:
            for client in self.waitclients:
                if client.id == id:
                    result = client
        elif select == 1:
            for client in self.chatclients_1:
                if client.id == id:
                    result = client
        elif select == 2:
            for client in self.chatclients_2:
                if client.id == id:
                    result = client
        elif select == 3:
            for client in self.chatclients_3:
                if client.id == id:
                    result = client
        elif select == 4:
            for client in self.chatclients_4:
                if client.id == id:
                    result = client
        elif select == 5:
            for client in self.chatclients_5:
                if client.id == id:
                    result = client

        return result


class ChatClient:   # 클라이언트를 상대하는 부분

    def __init__(self, room, current, socket):
        self.room = room  # 채팅방. Room 객체
        self.id = None  # 사용자 id
        self.current = current  # 사용자 위치
        self.socket = socket  # 사용자와 1:1 통신할 소켓

    def readMsg(self):

        try:
            self.id = self.socket.recv(1024).decode()
            # 계정명 설정
            self.room.sendMsgAll(self.room.showClients(self.current),self.current)
            self.room.sendMsgAll(self.room.summaryCount(),self.current)
            # 대기실 정보 최신화

            welcomemsg = self.id + "님 채팅방에 오신걸 환영합니다."

            while True:
                msg = self.socket.recv(1024).decode()  # 사용자가 전송한 메시지 읽음
                print(msg)
                if msg.startswith('/'):
                    if msg == '/help':
                        help_msg = "==========================\n명령어 목록\n"
                        help_msg += "/w : 귓속말 [유저] [메시지]\n"
                        help_msg += "==========================\n"
                        self.sendMsg(help_msg)
                        continue
                    elif msg == '/exit':  # 채팅방 나가기
                        self.room.addClient(self, 0)
                        self.room.delClient(self, self.current)
                        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.',self.current)
                        self.room.sendMsgAll(self.room.showClients(self.current),self.current)
                        self.current = 0
                        self.room.sendMsgAll(self.room.showClients(self.current),self.current)
                        self.room.sendMsgAll(self.room.summaryCount(),self.current)
                        # 채팅방 접속자 수 갱신
                        continue
                    elif msg == '/list':  # 접속유저 목록 호출 메뉴
                        self.sendMsg(self.room.showClients(self.current))
                        continue
                    elif msg == '/quit':  # 대기실 나가기 ( 해결 )
                        self.room.delClient(self,self.current)
                        self.room.sendMsgAll(self.room.showClients(self.current),self.current)
                        continue
                    elif msg.startswith('/w '):  # 귓말 명렁어 + 대상 빼고 뒷 메시지 보내기
                        targetUser = msg.split(' ')[1]
                        if self.id == targetUser:  # 귓말 대상을 자신에게 설정시
                            self.sendMsg("자기 자신에게는 귓속말을 할 수 없습니다.")
                            continue
                        elif self.room.checkClient(targetUser) == 1:  # 귓말 대상 존재 여부 조회
                            msg = msg[len(targetUser) + 4:]
                            msg = self.id + ' >>> ' + targetUser + ' : ' + msg
                            self.sendMsg(msg)
                            whisper = self.room.setWhipser(targetUser,self.current)
                            whisper.sendMsg(msg)
                            continue
                        else:  # 귓말 대상이 없을 때
                            self.sendMsg("해당 유저는 존재하지 않습니다.")
                            continue
                    else:
                        self.sendMsg("해당 명령어는 존재하지 않습니다.")
                        continue
                elif msg.startswith("select_room:"):
                    room = msg.split(":")[1]
                    enter_msg = self.id + '님이 입장하셨습니다.'
                    # 각 채팅방에 진입시 해당 채팅방의 인원 ++, 대기실 인원 --
                    if room == 1:
                        print("1번방 진입")
                        self.current = 1
                        self.room.addClient(self,1)
                        self.room.delClient(self,0)
                        self.sendMsg(welcomemsg, 1)
                        self.room.sendMsgExcept(enter_msg, 1)
                        self.room.sendMsgAll(self.room.showClients(1), 1)
                    elif room == 2:
                        self.current = 2
                        self.room.addClient(self, 2)
                        self.room.delClient(self, 0)
                        self.sendMsg(welcomemsg, 2)
                        self.room.sendMsgExcept(enter_msg, 2)
                        self.room.sendMsgAll(self.room.showClients(2), 2)
                    elif room == 3:
                        self.current = 3
                        self.room.addClient(self, 3)
                        self.room.delClient(self, 0)
                        self.sendMsg(welcomemsg, 3)
                        self.room.sendMsgExcept(enter_msg, 3)
                        self.room.sendMsgAll(self.room.showClients(3), 3)
                    elif room == 4:
                        self.current = 4
                        self.room.addClient(self, 4)
                        self.room.delClient(self, 0)
                        self.sendMsg(welcomemsg, 4)
                        self.room.sendMsgExcept(enter_msg, 4)
                        self.room.sendMsgAll(self.room.showClients(4), 4)
                    elif room == 5:
                        self.current = 5
                        self.room.addClient(self, 5)
                        self.room.delClient(self, 0)
                        self.sendMsg(welcomemsg, 5)
                        self.room.sendMsgExcept(enter_msg, 5)
                        self.room.sendMsgAll(self.room.showClients(5), 5)

                    continue

                msg = self.id + ' : ' + msg
                self.room.sendMsgAll(msg,self.current)  # 모든 사용자에 메시지 전송
        except Exception as e:
            print(e)
            main()

    def sendMsg(self, msg):     # 1대1 소켓
        self.socket.sendall(msg.encode(encoding="UTF-8"))

class ChatServer:
    ip = 'localhost'  # or 본인 ip or 127.0.0.1
    port = 9999

    def __init__(self):
        self.server_socket = None  # 서버 소켓(대문)
        self.room = Room()

    def open(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ChatServer.ip, ChatServer.port))
        self.server_socket.listen()

    def run(self):
        self.open()
        print('chatServer is Running...'.format(ChatServer.port))

        while True:
            client_socket, addr = self.server_socket.accept()
            print(addr, '접속')
            client = ChatClient(self.room, 0, client_socket)
            self.room.addClient(client,0)
            print('Client :', self.room.waitclients)
            th = threading.Thread(target=client.readMsg)
            th.start()

            # 접속 유저 없이도 서버를 유지 하기 위함
            # if threading.active_count() == 0:
            #     break

        # self.server_socket.close()
        # 접속된 유저 없어도 서버 유지를 위해 비활성화


def main():
    chatserver = ChatServer()
    chatserver.run()

main()
