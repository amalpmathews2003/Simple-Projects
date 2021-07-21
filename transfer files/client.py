import socket
import tqdm
import os

seperator="<SEPERATOR>"
buffer_size=4096  #send 4mb each time

host="192.168.43.22"
port =1448
file_path=r'C:\Users\amalp\OneDrive\Desktop\amal\Basic Electrical Engineering by D. P. Kothari, I. J. Nagrath (z-lib.org).pdf'

filesize=os.path.getsize(file_path)


#creating client socket
s=socket.socket()

#connecting to server
print(f"[+] connecting to {host}:{port}")
s.connect((host,port))
print(f"[+] connected")

#send the file_path and file_size
s.send(f"{file_path} {seperator} {filesize}".encode())


#send file

progress=tqdm.tqdm(range(filesize),f"sending {file_path}",unit="B",unit_scale=True,unit_divisor=1024)

with open(file_path,"rb") as f:
	while True:
		#read bytes from file
		bytes_read=f.read(buffer_size)
		if not bytes_read:
			break
		s.sendall(bytes_read)
		progress.update(len(bytes_read))
s.close()