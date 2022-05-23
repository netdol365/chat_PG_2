import socket, threading


class Room:  # 채팅방 클래스.
    def __init__(self):
        self.clients = []
        # self.allChat=None

    def addClient(self, client):  # 클라이언트 리스트 추가 후 스레드에 지정
        self.clients.append(client)

    def delClient(self, client):
        self.clients.remove(client)

    def sendMsgAll(self, msg):  # 채팅방에 있는 모든 사람한테 메시지 전송
        for client in self.clients:
            # print(i.id)
            # print(self.id)
            client.sendMsg(msg)

    def sendMsgExcept(self, msg):  # 채팅방에 있는 자신을 제외한 모든 사람한테 메시지 전송
        for client in self.clients:
            # print(type(i.id))
            if msg.find(client.id) == -1:
                client.sendMsg(msg)

    def showClients(self):
        result = "==========================\n접속 유저\n"
        count = 0
        for client in self.clients:
            count += 1
            result += str(count) + " : " + client.id + "\n"
        result += "참여자 수 : " + str(count) + " 명입니다.\n"
        result += "==========================\n"
        return result

    def checkClient(self, id):
        judge = 0
        for i in self.clients:
            if i.id == id:
                judge = 1
        return judge

    def setWhipser(self, id):
        result = ""
        for client in self.clients:
            if client.id == id:
                result = client
        return result


class ChatClient:

    def __init__(self, room, socket):
        self.room = room  # 채팅방. Room 객체
        self.id = None  # 사용자 id
        self.socket = socket  # 사용자와 1:1 통신할 소켓

    def readMsg(self):
        self.id = self.socket.recv(1024).decode()

        if self.id.isspace():
            self.sendMsg("닉네임을 지정해주셔야 합니다.\n(공란 불가)")
            while True:
                self.id = self.socket.recv(1024).decode()
                print(self.id)
                if not self.id.isspace():
                    break
                else:
                    self.sendMsg("닉네임을 지정해주셔야 합니다.\n(공란 불가)")

        # 환영 메시지 출력
        welcomemsg = self.id + "님 채팅방에 오신걸 환영합니다."
        welcomemsg_byte = welcomemsg.encode("UTF-8")
        self.socket.sendall(welcomemsg_byte)

        msg = self.id + '님이 입장하셨습니다'
        self.room.sendMsgExcept(msg)

        try:
            while True:
                msg = self.socket.recv(1024).decode()  # 사용자가 전송한 메시지 읽음
                if msg == '/help':
                    help_msg = "==========================\n명령어 목록\n"
                    help_msg += "/exit : 채팅 종료\n/list : 접속 유저 확인\n/w : 귓속말 [유저] [메시지]\n"
                    help_msg += "==========================\n"
                    self.sendMsg(help_msg)
                    continue
                elif msg == '/exit':  # 종료 메시지이면 루프 종료
                    quit_msg = "채팅을 종료합니다."
                    self.sendMsg(quit_msg)  # 이 메시지를 보낸 한명에게만 전송
                    self.room.delClient(self)
                    break
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
                        
                msg = self.id + ' : ' + msg
                self.room.sendMsgAll(msg)  # 모든 사용자에 메시지 전송
        except Exception as e:
            print(e)
            chatserver = ChatServer()
            chatserver.run()
            
            
        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')

    def sendMsg(self, msg):
        # print(type(msg))
        self.socket.sendall(msg.encode(encoding='utf-8'))


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
        print('Server is Running...')

        while True:
            client_socket, addr = self.server_socket.accept()
            print(addr, '접속')
            client = ChatClient(self.room, client_socket)
            self.room.addClient(client)
            print('Client :', self.room.clients)
            th = threading.Thread(target=client.readMsg)
            th.start()
            
        # 접속 유저 없이도 서버유지
        #     if threading.active_count() == 0:
        #         break
        # 
        # self.server_socket.close()


def main():
    chatserver = ChatServer()
    chatserver.run()


main()
