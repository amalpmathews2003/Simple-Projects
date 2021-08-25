import socket
#import threading
#import tqdm
from tkinter import *
from tkinter.ttk import*
from tkinter.filedialog import askopenfilename
import os
import time
import concurrent.futures


class FileTransfer(object):
    """Class for filetransfering with the help
       of socket module.threading is done by concurrent.futures module
       so that to return values from function more easily
       (tqdm module is used only for representation purpose(prograss bar)) 
       
    """
    def __init__(self, host, port,filepath=None, nickname=None,socket=None):
        self.buffersize = 1024
        self.host = host
        self.port = port
        if filepath:
            self.filepath=filepath
            self.filename = os.path.basename(self.filepath)
            self.filesize = os.path.getsize(self.filepath)
            print(self.filepath)
            print(self.filename)
            print(self.filesize)
        if socket:
            self.socket = socket
        if nickname:
            self.nickname = nickname
        print('class initiated')

    def send_file(self):
        with concurrent.futures.ThreadPoolExecutor() as executer:
            #t=executer.submit(self.send_file_main)
            t=executer.submit(self.recieve_connections)
            return t.result()

    def recieve_file(self):
        with concurrent.futures.ThreadPoolExecutor() as executer:
            t=executer.submit(self.recieve_file2)
            return t.result()

   
    def recieve_connections(self):
        print(self.host,self.port,"recieve_connections")
        #self.socket.bind((self.host,self.port))
        self.socket.listen()

        client,_=self.socket.accept()
        self.send_file2(client)
        self.socket.close()


    def send_file2(self,client):
        print('send_file2')
        client.sendall(repr(["#1021#", self.nickname, self.filename, self.filesize]).encode())
        t=[]
        begin=time.time()
        with open(self.filepath, "rb") as f:
            while True:
                if time.time()-begin>1:
                    break
                try:
                    bytes_read = f.read(self.buffersize)
                    if len(bytes_read)>0:
                        t.append(len(bytes_read))
                        begin=time.time()
                        client.sendall(bytes_read)
                        #print(len(bytes_read))
                        progress.update(len(bytes_read))
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    #print(e)
                    pass

    def recieve_file2(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        li = eval(self.socket.recv(1024).decode())
        sender, filename, filesize = li[1:]
        t=[]
        begin=time.time()
        with open(filename, "wb") as f:
            while True:
                if time.time()-begin>1:
                    break
                try:  
                    bytes_read = self.socket.recv(self.buffersize)
                    if len(bytes_read)>0:
                        t.append(len(bytes_read))
                        begin=time.time()
                        #print(len(bytes_read))
                        f.write(bytes_read)
                        #progress.update(len(bytes_read))
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    #print(e)
                    pass
        self.socket.close()
        return filename
    
    def send_file_main(self):
        print('send_file_main')
        self.socket.connect((self.host, self.port))
        self.socket.sendall(
            repr(["#1021#", self.nickname, self.filename, self.filesize]).encode())
        #progress = tqdm.tqdm(range(
        #    self.filesize), f"sending {self.filename}", unit="B", unit_scale=True, unit_divisor=1024)
        t=[]
        begin=time.time()
        with open(self.filepath, "rb") as f:
            while True:
                if time.time()-begin>1:
                    break
                try:
                    bytes_read = f.read(self.buffersize)
                    if len(bytes_read)>0:
                        t.append(len(bytes_read))
                        begin=time.time()
                        self.socket.sendall(bytes_read)
                        #print(len(bytes_read))
                        progress.update(len(bytes_read))
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    #print(e)
                    pass
        print(len(t))
        self.socket.close()
        return [self.host, self.port, "file sent"]

    def recieve_file_main(self):
        print('recieve_file_main')
        print(self.host,self.port)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        client, _ = self.socket.accept()
        li = eval(client.recv(1024).decode())
        sender, filename, filesize = li[1:]
        #progress = tqdm.tqdm(range(
        #    filesize), f"Recieving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        t=[]
        begin=time.time()
        with open(filename, "wb") as f:
            while True:
                if time.time()-begin>1:
                    break
                try:  
                    bytes_read = client.recv(self.buffersize)
                    if len(bytes_read)>0:
                        t.append(len(bytes_read))
                        begin=time.time()
                        #print(len(bytes_read))
                        f.write(bytes_read)
                        progress.update(len(bytes_read))
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    #print(e)
                    pass
        print(len(t))
        client.close()
        self.socket.close()
        return [self.host, self.port, "file recieved"]
        

if __name__ == '__main__':
   # ob = FileTransfer("127.0.0.1", 55550, "amal")
   # ob.send_file()
   
   print(help(FileTransfer))