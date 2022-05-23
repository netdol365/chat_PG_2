import socket, threading


class Room:  # 채팅방 클래스.
    def __init__(self):
        self.clients = []

    def addClient(self, client):  # 클라이언트 리스트 추가 후 스레드에 지정
        self.clients.append(client)

    def delClient(self, client):
        self.clients.remove(client)

    def sendMsgAll(self, msg):  # 채팅방에 있는 모든 사람한테 메시지 전송
        for client in self.clients:
            client.sendMsg(msg)

    def sendMsgExcept(self, msg):  # 채팅방에 있는 자신을 제외한 모든 사람한테 메시지 전송
        for client in self.clients:
            if msg.find(client.id) == -1:
                client.sendMsg(msg)

    def showClients(self):        # 채팅방 접속자들 목록 출력
        result = "Client_Count"
        for client in self.clients:
            result += "\n" + client.id
        return result

    def checkClient(self, id):    # id와 일치 여부 판별
        judge = 0
        for i in self.clients:
            if i.id == id:
                judge = 1
        return judge

    def setWhipser(self, id):       # 귓속말 상대 설정
        result = ""
        for client in self.clients:
            if client.id == id:
                result = client
        return result


class ChatClient:   # 클라이언트를 상대하는 부분

    def __init__(self, room, socket):
        self.room = room  # 채팅방. Room 객체
        self.id = None  # 사용자 id
        self.fruits = None
        self.socket = socket  # 사용자와 1:1 통신할 소켓

    def readMsg(self):

        self.id = self.socket.recv(1024).decode()
        # 채팅방 접속 정보 갱신

        welcomemsg = self.id + "님 채팅방에 오신걸 환영합니다."

        self.sendMsg(welcomemsg)

        msg = self.id + '님이 입장하셨습니다'
        self.room.sendMsgExcept(msg)
        self.room.sendMsgAll(self.room.showClients())
        # 환영 메시지 출력 및 접속자 정보 갱신

        print("메시지 수신 대기중...")
        # 연결 여부 확인 용도
        while True:
            try:
                msg = self.socket.recv(1024).decode()  # 사용자가 전송한 메시지 읽음
                print(msg)
                if msg.find('/') == 0:
                    if msg == '/help':
                        help_msg = "==========================\n명령어 목록\n"
                        help_msg += "/w : 귓속말 [유저] [메시지]\n"
                        help_msg += "==========================\n"
                        self.sendMsg(help_msg)
                        continue
                    elif msg == '/exit':  # 종료 메시지이면 루프 종료
                        quit_msg = "채팅을 종료합니다."
                        self.sendMsg(quit_msg)  # 이 메시지를 보낸 한명에게만 전송
                        self.room.delClient(self)
                        self.sendMsg(self.room.showClients())
                        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')
                        self.room.sendMsgAll(self.room.showClients())
                        # 채팅방 접속자 수 갱신
                        continue
                    elif msg == '/list':  # 접속유저 목록 호출 메뉴
                        self.sendMsg(self.room.showClients())
                        continue
                    elif msg.find('/w ') != -1:  # 귓말 명렁어 + 대상 빼고 뒷 메시지 보내기
                        targetUser = msg.split(' ')[1]
                        if self.id == targetUser:  # 귓말 대상을 자신에게 설정시
                            self.sendMsg("자기 자신에게는 귓속말을 할 수 없습니다.")
                            continue
                        elif self.room.checkClient(targetUser) == 1:  # 귓말 대상 존재 여부 조회
                            msg = msg[len(targetUser) + 4:]
                            msg = self.id + ' >>> ' + targetUser + ' : ' + msg
                            self.sendMsg(msg)
                            whisper = self.room.setWhipser(targetUser)
                            whisper.sendMsg(msg)
                            continue
                        else:  # 귓말 대상이 없을 때
                            self.sendMsg("해당 유저는 존재하지 않습니다.")
                            continue
                    else:
                        self.sendMsg("해당 명령어는 존재하지 않습니다.")
                        continue

                msg = self.id + ' : ' + msg
                self.room.sendMsgAll(msg)  # 모든 사용자에 메시지 전송
            except Exception as e:
                print(e)
                chatsever = ChatServer()
                chatsever.run()

    def sendMsg(self, msg):     # 1대1 소켓
        self.socket.sendall(msg.encode(encoding="UTF-8"))


class ChatServer:
    ip = 'localhost'  # or 본인 ip or 127.0.0.1
    port = 4444
    # 채팅방4과의 연결

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
        print('chatServer1 is Running...')

        while True:
            client_socket, addr = self.server_socket.accept()
            print(addr, '접속')
            client = ChatClient(self.room, client_socket)
            self.room.addClient(client)
            print('Client :', self.room.clients)
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
