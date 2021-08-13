from tkinter import*
import time
import sounddevice as sd
import wavio 
import threading
class AudioRecorder(object):
	"""docstring for AudioRecorder"""
	def __init__(self,start_btn,stop_btn,nickname):
		self.start=0
		self.end=0
		self.recording=0
		self.max_duration=20
		self.freq=44400
		self.start_btn=start_btn
		self.stop_btn=stop_btn
		self.nickname=nickname

	def start_recording(self):
		self.create_thread(self.start_recording_main)
	def stop_recording(self):
		self.stop_recording_main()
		#self.play_recording()
	def play_recording(self):
		self.create_thread(self.play_recording_main)
		#self.save_recording()
	def save_recording(self):
		self.save_recording_main()

	def create_thread(self,function):
		t=threading.Thread(target=function)
		t.start()

	def start_recording_main(self):
		self.start=time.time()
		self.start_btn.configure(state=DISABLED)
		self.stop_btn.configure(state=NORMAL)
		self.recording=sd.rec(self.max_duration*self.freq,
			samplerate=self.freq,channels=2)
	def stop_recording_main(self):
		self.end=time.time()
		time_elapsed=self.end-self.start
		#print(time_elapsed)
		#print(len(self.recording))
		self.recording=self.recording[:int(time_elapsed*self.freq)]
		#print(len(self.recording))
		self.start_btn.configure(state=NORMAL)
		self.stop_btn.configure(state=DISABLED)
		sd.stop()
	def play_recording_main(self):
		sd.playrec(data=self.recording,samplerate=self.freq,channels=2)
		sd.wait()

	def save_recording_main(self):
		file_name=f"{self.nickname}_{str(time.ctime())[11:19]}"
		print(file_name)
		wavio.write('temp.wav',self.recording,self.freq,sampwidth=2)
		return file_name


		
if __name__ == '__main__':	
	root=Tk()
	root.geometry('300x300')

	b1=Button(root,text="start")
	b2=Button(root,text="stop")
	b3=Button(root,text="play")
	b4=Button(root,text="save")
	ar=AudioRecorder(b1,b2,"amal")
	b1.configure(command=ar.start_recording)
	b2.configure(command=ar.stop_recording)
	b3.configure(command=ar.play_recording) 
	b4.configure(command=ar.save_recording)

	b1.pack()
	b2.pack()
	b3.pack()
	b4.pack()

	root.mainloop()
