import threading
import socket
import tkinter as tk


class UiChatClient:
    ip = 'localhost'
    port = 9999

    def __init__(self):
        self.conn_socket = None  # 서버와 연결된 소켓
        self.win = None
        self.chatCont = None
        self.myChat = None
        self.sendBtn = None
        self.allChat =''

    def conn(self):
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_socket.connect((UiChatClient.ip, UiChatClient.port))

    def setWindow(self):
        self.win = tk.Tk()
        self.win.title('채팅프로그램')
        self.win.geometry('400x500+100+100')
        self.chatCont = tk.Label(self.win, width=50, height=30, text='닉네임을 설정해주세요')
        self.myChat = tk.Entry(self.win, width=40)
        self.sendBtn = tk.Button(self.win, width=10, text='전송', command=lambda : self.sendMsg())

        self.chatCont.grid(row=0, column=0, columnspan=2)
        self.myChat.grid(row=1, column=0, padx=10)
        self.sendBtn.grid(row=1, column=1)

    def sendMsg(self):  # 키보드 입력 받아 상대방에게 메시지 전송
        msg = self.myChat.get()
        self.myChat.delete(0, tk.END)
        self.myChat.config(text='')
        msg = msg.encode(encoding='utf-8')
        print(self.conn_socket)
        self.conn_socket.sendall(msg)
        print('전송')

    def recvMsg(self):  # 상대방이 보낸 메시지 읽어서 화면에 출력
        while True:
            print('접속완료')
            msg = self.conn_socket.recv(1024)
            msg = msg.decode()+'\n'
            self.allChat += msg
            print(',:', self.allChat)

            self.chatCont.config(text=self.allChat)

            if msg.find("채팅을 종료합니다.") != -1:
                self.close()
                break

    def run(self):
        self.conn()
        self.setWindow()

        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.win.mainloop()

    def close(self):
        self.conn_socket.close()
        print('종료되었습니다')


def main():
    conn = UiChatClient()
    conn.run()


main()