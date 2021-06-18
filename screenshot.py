import pyscreenshot
import time
from tkinter import *
from tkinter.filedialog import asksaveasfilename


image=pyscreenshot.grab()
#wn=Tk()

x=str(time.asctime(time.localtime(time.time())))
x=x.replace(':','-')

path=asksaveasfilename(initialfile=x,defaultextension=".png",filetypes=[("Image","*.png")])



image.save(f"{path}")

