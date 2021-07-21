import socket
import tqdm
import os

seperator="<SEPERATOR>"
buffer_size=4096 #send 4mb each time

host="0.0.0.0"
port =1448


#create server rocket
s=socket.socket()
s.bind((host,port))
s.listen(5)
print(f"[*] Listening as {host}:{port}")

client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

received = client_socket.recv(buffer_size).decode()
filename, filesize = received.split(seperator)
filename = os.path.basename(filename)
filesize = int(filesize)


#receive file

progress =tqdm.tqdm(range(filesize),f"Recieving {filename}",unit="B",unit_scale=True,unit_divisor=1024)
with open(filename,"wb") as f:
	while True:
		bytes_read=client_socket.recv(buffer_size)
		if not bytes_read:
			break
		f.write(bytes_read)
		progress.update(len(bytes_read))

client_socket.close()
s.close
