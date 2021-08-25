import threading
import socket
import time

host = "192.168.43.12"
port = 55556


class ServerClass():
    """docstring for ServerClass"""

    """
	Communication:
		server and clients are communicating by sending list(in binary)
		[code,sender,reciever,message,etc]
	Keywords:
		#1000#-Accept connctions
		#1001#-Welcome message
		#1010#-Public message
		##1099#-Offline message
		#1091# -joined the chat
		#1090#-active nicknames
		#1011#-Private message
		#1021#-file_transfer public
		#1071#-audio file
	"""

    def __init__(self):
        super(ServerClass, self).__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        print(host, port)
        print("Server is listening")
        self.clients = []  # contains clients which are online
        self.nicknames = []  # contains nickname(username) of each client
        self.recieve_connections()

    def find_nickname(self, client):
        index = self.clients.index(client)
        return self.nicknames[index]

    def find_client(self, nickname):
        index = self.nicknames.index(nickname)
        return self.clients[index]

    def send_message_to_all(self, message):
        if(message[1] == "host"):
            sender = "host"
        else:
            sender = self.find_client(message[1])
        message = repr(message)
        for client in self.clients:
            if client != sender:
                client.sendall(message.encode())

    def send_message_to_individual(self, sender, reciever, message):
        # sender and reciver will be nicknames
        reci = self.find_client(reciever)
        reci.sendall(repr(["#1011#", sender, reciever, message]).encode())

    def handle_client(self, client):
        while True:
            try:
                message = eval(client.recv(1024).decode())

                if(message[0] == "#1010#"):
                    self.send_message_to_all(message)
                elif message[0] == "#1011#":

                    self.send_message_to_individual(
                        message[1], message[2], message[3])
                elif message[0] == "#1021#":
                    print(f'{message[1]} file sending')
                    try:
                        self.send_message_to_all(["#1021#", message[1], message[2], f"{message[1]} is sending file", message[4], message[5], message[6]])
                    except:
                        self.send_message_to_all(["#1021#", message[1], message[2], f"{message[1]} is sending file", message[4], message[5]])

                else:
                    print(message)
            except Exception as e:
                print(e)
                index = self.clients.index(client)
                self.clients.remove(client)
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                offline_mess = ["#1010#", "host", "ALL", f'{nickname} is offline']
                print(offline_mess)
                self.send_message_to_all(offline_mess)
                self.send_message_to_all(
                    ["#1090#", "host", "ALL", self.nicknames])
                break

    def recieve_connections(self):
        while True:
            client, address = self.server.accept()
            connect_mess = repr(
                ['#1000#', "host", "client", "Enter the Nickname"])
            client.sendall(connect_mess.encode())
            nickname = client.recv(1024).decode()
            nickname = eval(nickname)[3]
            self.clients.append(client)
            self.nicknames.append(nickname)
            print(f'Server is connected with {str(address)} as {nickname}')
            welcome_mess = repr(
                ['#1010#', "host", nickname, "You are connected"])
            client.sendall(welcome_mess.encode())
            time.sleep(0.5)
            self.send_message_to_all(["#1091#", nickname, "ALL", f'{nickname} joined the chat', nickname])
            time.sleep(0.5)
            client.sendall(
                repr(["#1090#", "host", nickname, self.nicknames]).encode())
            client_thread = threading.Thread(
                target=self.handle_client, args=(client,))
            client_thread.start()


ServerClass()