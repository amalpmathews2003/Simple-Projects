import threading
import socket
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import platform
import time
from audio import AudioRecorder
from file import FileTransfer
from playsound import playsound
from PIL import Image,ImageTk
host = "192.168.43.12"
port = 55556
# ports used 55556,55556+1


class ClientClass():
    """docstring for ClientClass"""

    def __init__(self):
        self.nickname = "AMAL"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.active_nicknames = 4*["amal", "aleena", "asha", "amal2", "aleena2", "asha2",
                                 "amal3", "aleena3", "asha3", "amal4", "aleena4", "asha4", "amal5", "aleena5", "asha5", "amal6", "aleena6", "asha6"]
        self.active_nicknames = [""]
        self.os=platform.system()
        self.start_window()
        #self.open_main_window()

    def open_main_window(self):
        start = time.time()
        self.main_window = Tk()
        self.main_window.title(f'{self.nickname}')
        self.main_window.geometry('600x600')
        super(ClientClass, self).__init__()
        """
            All incoming and outgoing message will appear hear
        """

        message_window_frame = Frame(self.main_window)
        message_window_frame.configure(width=400, height=500)
        message_window_frame.place(x=0, y=0)

        """
            People online will appear here
        """
        clients_online_frame = Frame(self.main_window)
        clients_online_frame.configure(width=200, height=400)
        clients_online_frame.place(x=400, y=0)
        """
            space for writing messages
        """

        text_type_frame = Frame(self.main_window)
        text_type_frame.configure(width=400, height=100)
        text_type_frame.place(x=0, y=500)

        self.send_btn = Button(self.main_window, text="Send",
                               command=self.send_message_to_server)
        photo = PhotoImage(file=r"images/send_icon.png")
        photoimage = photo.subsample(5, 5)
        self.send_btn.configure(image=photoimage,
                                compound=BOTTOM)
        self.send_btn.place(x=400, y=500)
        


        self.message_win_canvas=Canvas(message_window_frame,width=360,height=450)
        self.message_win_canvas.configure(bd=10,bg="red",highlightcolor="blue")
        scroll=Scrollbar(message_window_frame)
        scroll.pack(side=RIGHT,fill=Y)
        self.message_ouput_frame=Frame(self.message_win_canvas)
        self.message_ouput_frame.bind("<Configure>",lambda e:self.message_win_canvas.configure(scrollregion=self.message_win_canvas.bbox('all')))
        self.message_win_canvas.create_window(0,0,window=self.message_ouput_frame,anchor="nw")
        self.message_win_canvas.update_idletasks()
        self.message_win_canvas.configure(yscrollcommand=scroll.set,scrollregion=self.message_win_canvas.bbox('all'))

        s=Style()
        s.configure('1.TLabel',background="#DB9719",foreground="black",font=20)
        self.message_win_canvas.pack(side=LEFT,fill=BOTH,expand=True)
        scroll.configure(command=self.message_win_canvas.yview)
        
        # for i in range(100):
        #     l=Label(self.message_ouput_frame,text="hello how are you "*1,relief=GROOVE,anchor=CENTER,wrap=0,style="1.TLabel")
        #     l.pack()
        self.message_win_canvas.update_idletasks()
        self.message_win_canvas.yview_moveto(1.0)


        users_online_canvas = Canvas(
            clients_online_frame, height=300, width=180)
        scrollbar = Scrollbar(clients_online_frame)
        scrollbar.pack(fill=Y, side=RIGHT)
        self.clients_online_frame2 = Frame(users_online_canvas)
        st = Style()
        st.configure("W.TButton", foreground="green", borderwidth=0)

        self.update_users_online()
        users_online_canvas.create_window(
            0, 0, window=self.clients_online_frame2)
        users_online_canvas.update_idletasks()
        users_online_canvas.configure(scrollregion=users_online_canvas.bbox('all'),
                                           yscrollcommand=scrollbar.set)
        users_online_canvas.pack()
        scrollbar.config(command=users_online_canvas.yview)
        # mouse binding

        def _on_mousewheel_online_canvas_linux(event):
            if(event.num == 4):
                users_online_canvas.yview_scroll(10, "units")
            else:
                users_online_canvas.yview_scroll(-10, "units")

        def _on_mousewheel_windows_online_canvas(event):
            users_online_canvas.yview_scroll(
                int(-1 * event.delta / 120), 'units')

        def _on_mousewheel_message_canvas_linux(event):
            if(event.num == 4):
                self.message_win_canvas.yview_scroll(10, "units")
            else:
                self.message_win_canvas.yview_scroll(-10, "units")

        def _on_mousewheel_message_online_canvas(event):
            self.message_win_canvas.yview_scroll(
                int(-1 * event.delta / 120), 'units')

        if(self.os== "Linux"):
            # for linux
            users_online_canvas.bind("<Button-4>", _on_mousewheel_online_canvas_linux)
            self.message_win_canvas.bind("<Button-4>", _on_mousewheel_message_canvas_linux)
            users_online_canvas.bind("<Button-5>", _on_mousewheel_online_canvas_linux)
            self.message_win_canvas.bind("<Button-5>", _on_mousewheel_message_canvas_linux)

        elif(self.os == 'Windows'):
            users_online_canvas.bind(
                "<MouseWheel>", _on_mousewheel_windows_online_canvas)
            self.message_win_canvas.bind(
                "<MouseWheel>", _on_mousewheel_message_online_canvas)

        self.message_input_textbox = scrolledtext.ScrolledText(text_type_frame)
        self.message_input_textbox.configure(
            fg="black", bg="white", bd=3, width=47, height=5, state=NORMAL,wrap=CHAR)
        self.message_input_textbox.place(x=0, y=0)
        self.message_input_textbox.focus()

        self.mic_on = Button(self.main_window, text="ON", width=4)
        self.mic_off = Button(self.main_window, text="OFF", width=5)
        mic_object = AudioRecorder(self.mic_on, self.mic_off, self.nickname)
        photo2 = PhotoImage(file=r"images/mic_icon.png")
        photo2 = photo2.subsample(10, 10)
        self.mic_on.configure(image=photo2, state=NORMAL, style='TButton',
                              command=mic_object.start_recording)
        self.mic_off.configure(image=photo2, state=DISABLED,
                               style='TButton', command=lambda:self.mic_stop_recording(mic_object))
        self.mic_off.place(x=550, y=500)
        self.mic_on.place(x=500, y=500)

        file_btn = Button(self.main_window, text="file", width=5)
        file_btn.configure(command=self.file_transfer_send)
        file_btn.place(x=500, y=550)
        end = time.time()
        print(f'gui made in {end-start} seconds')

        t1 = threading.Thread(target=self.recieve_message_from_server)
        t1.start()

        self.main_window.mainloop()

    def mic_stop_recording(self,mic_object):
        file_name=mic_object.stop_recording()
        def play_music(filename):
                playsound(filename)
        def play(filename):
            t=threading.Thread(target=play_music,args=(filename,))
            t.start()
        photo2 = PhotoImage(file=r"images/speaker_icon.png")
        photo2 = photo2.subsample(10, 10)
        b=Button(self.message_ouput_frame,text=f"{file_name}  ",command=lambda:play(file_name),image=photo2,compound=RIGHT)
        b.pack()
        self.file_transfer_send(filepath=file_name,type="#1071#")


    def get_free_port():
        s=range(port+1,port+20)
        soc=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.connect(('8.8.8.8',80))
        myip=soc.getsockname()[0]
        # for i in s:
        #     try:
        #         socket1.connect((myip,i))
        #     except:
        #         break
        # return (myip,i)
        socket1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket1.bind((myip,0))
        port2=socket1.getsockname()[1]
        return (myip,port2,socket1)
    def load_thumbnail(self,filepath):
        try:
            im=Image.open(filepath)
            im.thumbnail((200,200))
            im=ImageTk.PhotoImage()
            l=Label(self.message_ouput_frame,image=image)
            l.pack(fill=BOTH,expand=True)
        except:
            pass



    def file_transfer_send(self,filepath=None,type=None):
        if filepath==None:
            filepath = askopenfilename(
                title="select", filetypes=[('All', "*.*")])
        if filepath:
            self.load_thumbnail(filepath)
            myip,port,socket1=ClientClass.get_free_port()
            message=["#1021#", self.nickname, "ALL", "sending file",myip,port]
            if type=="#1071#":
                message.append("#1071#")
            
            self.client.sendall(repr(message).encode())
            file_object = FileTransfer(myip, port, filepath, self.nickname,socket1)
            val=file_object.send_file()
            print(val)

    def file_transfer_recieve(self,host,port,type=None):
        print('file recieveing')
        file_object = FileTransfer(host, port)
        file_name=file_object.recieve_file()
        print(file_name)
        if type=="#1071#":
            def play_music(filename):
                playsound(filename)
            def play(filename):
                t=threading.Thread(target=play_music,args=(filename,))
                t.start()
            photo2 = PhotoImage(file=r"images/speaker_icon.png")
            photo2 = photo2.subsample(10, 10)
            b=Button(self.message_ouput_frame,text=f"{file_name}  ",command=lambda:play(file_name),image=photo2,compound=RIGHT)
            b.pack()
    def start_window(self):
        start = Tk()
        start.title("Start")
        l = Label(start, text="Enter Your Nickname")
        l.place(x=10, y=10)
        nickname = Text(start, width=20, height=1)
        nickname.place(x=10, y=40)
        nickname.focus()
        confirm_btn = Button(start, text="Confirm", command=lambda: self.set_nickname(
            nickname.get("1.0", END), start))
        confirm_btn.place(x=45, y=80)
        start.mainloop()

    def set_nickname(self, nickname, start_window):
        start_window.destroy()
        self.nickname = nickname[:-1]
        print(self.nickname)
        self.open_main_window()

    def update_message_window(self, sender, message, private=False):
        if private:
            l=Label(self.message_ouput_frame,text=f'{sender} (privately)=:\n{message}\n',style="1.TLabel")
        else:
            l=Label(self.message_ouput_frame,text=f'{sender} =:\n{message}\n',style="1.TLabel")
        l.pack()
        if sender=="me":
            l.configure(justify=LEFT,width=32,wraplength=0)
        else:
            l.configure(justify=LEFT,width=32,wraplength=0)
        self.message_win_canvas.update_idletasks()
        self.message_win_canvas.yview_moveto(1.0)
        self.message_input_textbox.focus()

    def update_users_online(self):

        for widget in self.clients_online_frame2.winfo_children():
            widget.destroy()

        for i in range(len(self.active_nicknames)):
            def insert(x=self.active_nicknames[i]):
                self.message_input_textbox.insert(END, str(x) + ":::")
            b = Button(self.clients_online_frame2, text=str(
                self.active_nicknames[i]), command=insert, style="W.TButton")
            b.pack()
        
    """
        socket connections
    """

    def recieve_message_from_server(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                message = eval(message)
                if(message[0] == "#1000#"):
                    self.client.sendall(
                        repr(["#1000#", self.nickname, "host", self.nickname]).encode())
                elif message[0] == "#1010#":
                    self.update_message_window(message[1], message[3])
                elif message[0]=="#1011#":
                    self.update_message_window(message[1], message[3],1)
                elif message[0] == "#1090#":
                    self.active_nicknames = message[3]
                    self.update_users_online()
                elif message[0] == "#1091#":
                    self.update_message_window("", message[3])
                    self.active_nicknames.append(message[4])
                    self.update_users_online()
                elif message[0] == "#1091#":
                    self.update_message_window(message[1], message[3], True)
                elif message[0]=="#1021#":
                    print(message)
                    self.update_message_window("", message[2])
                    if "#1071#" in message:
                        self.file_transfer_recieve(message[4],message[5],message[6])
                    else:
                        self.file_transfer_recieve(message[4],message[5])
                else:
                    print(message)
            except Exception as e:
                print(f"Unknown error occured|{e}")
                self.client.close()
                break

    def send_message_to_server(self):
        recever="ALL"
        message_text = self.message_input_textbox.get("1.0", END)
        if(message_text == "" or message_text is None):
            return
        self.message_input_textbox.delete("1.0", END)
        message_text = message_text[:-1]

        if ":::" in message_text:#provate message
            t=message_text.split(":::")
            recever=t[0]
            message_text=t[1]

        t1,t2="",""
        if (len(message_text)>32):
            for i in range(len(message_text)):
                t2+=message_text[i]
                if i%32==1 and i!=1:
                    t1+=(t2+"\n")
                    t2=""
            message_text=t1+t2+"\n"
            t1=""
            t2=""
        
        if recever=="ALL":
            self.update_message_window("me", message_text)
            message = repr(["#1010#", self.nickname, "ALL", message_text])
            self.client.sendall(message.encode())
        else:
            self.update_message_window(f"me->{recever} ", message_text)
            message = repr(["#1011#", self.nickname, recever, message_text])
            self.client.sendall(message.encode())


ClientClass()