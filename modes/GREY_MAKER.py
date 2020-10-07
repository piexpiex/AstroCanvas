import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from tkinter import *
import sys
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def GREY_IMAGES(self,master):
	#-------Imagen grey----------

	#Selection contrast and Stretch
	#qa=100
	#st=1
	self.qa_text=Label(master,text='Contrast',width=10,bg='grey')
	self.qa_text.pack()
	self.qa_text.place(x=10,y=350)
	self.qa_get=Scale(master,from_=1,orient=HORIZONTAL,to=1000,resolution=10,width=10,sliderlength=10,length=200,bg='grey')
	self.qa_get.pack()
	self.qa_get.place(x=100,y=350)
	self.st_text=Label(master,text='Strength',width=10,bg='grey')
	self.st_text.pack()
	self.st_text.place(x=10,y=400)
	self.st_get=Scale(master,from_=0,orient=HORIZONTAL,to=100,resolution=0.1,width=10,sliderlength=10,length=200,bg='grey') #orient=HORIZONTAL,
	self.st_get.pack()
	self.st_get.place(x=100,y=400)
	
	self.GREY_MAKER_text=Label(master,text='GREY MAKER',width=45,bg='grey')
	self.GREY_MAKER_text.pack()
	self.GREY_MAKER_text.place(x=10,y=470)
	self.grey_text=Label(master,text='grey image',width=10,bg='grey')
	self.grey_text.pack()
	self.grey_text.place(x=10,y=500)
	self.grey_get=Entry(master,bg='grey',width=40)
	self.grey_get.insert(0,'Filter_i-0-.fits')
	self.grey_get.pack()
	self.grey_get.place(x=90,y=500)

	def read_image(image):
		image_name=str(image)
		if image_name[len(image_name)-5:]=='.fits':
			image_data=fits.open(image_name)[0].data
		else:
			print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS') 
		return(image_data)


	def grey_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
			
		grey=self.grey_get.get()
		
		grey=read_image(grey)
		st=self.st_get.get()
		st_float=float(st)
		
		qa=self.qa_get.get()
		qa_float=float(qa)

		grey_x_1,grey_x_2,grey_y_1,grey_y_2=0,0,0,0
		#Selection of scale
		Scale=scale.get() #Scale=input('Scale')
		if Scale=='linear':
			pass
		elif Scale=='logaritmic':
			grey=np.log10(grey+1)

		#Normalization of each image and plotting
		#r=r[r_x_1:r_x_2,r_y_1:r_y_2]
		grey_max=max(np.amax(grey,axis=0))
		grey=grey/grey_max
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		if qa<10:
			qa=1
		im = ax.imshow(grey,vmin=(np.mean(grey)-np.std(grey)-st)/qa,vmax=(np.mean(grey)+np.std(grey)+st)/qa, interpolation='nearest', origin='lower', cmap='gray',aspect='auto')
		fig.set_size_inches(4.5,4.5)
		
		#fig.savefig('test2png.png', dpi=100)
		self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	
		#toolbar = NavigationToolbar2Tk(canvas, master)
		#toolbar.update()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		#plt.show()

	fig, ax = plt.subplots()
	fig.set_size_inches(4.5, 4.5)
	axoff_fun = np.vectorize(lambda ax:ax.axis('off'))
	# ... stuff here ...
	axoff_fun(ax)
	#fig.savefig('test2png.png', dpi=100)
	self.Canvas_text=Label(master,text='CURRENTLY IMAGE',width=64,bg='grey')
	self.Canvas_text.pack()
	self.Canvas_text.place(x=400,y=100)
	self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
	self.canvas.draw()
	#toolbar = NavigationToolbar2Tk(canvas, master)
	#toolbar.update()
	self.canvas.get_tk_widget().place(x=400,y=150)
	


	scale = StringVar(master)
	scale.set("linear") # initial value

	self.Scale_text=Label(master,text='Scale',width=10,bg='grey')
	self.Scale_text.pack()
	self.Scale_text.place(x=10,y=300)
	self.Scale_get = OptionMenu(master, scale, 'logaritmic', 'linear')
	self.Scale_get.config(width=10,bg='grey',highlightthickness=0)
	self.Scale_get.pack()
	self.Scale_get.place(x=100,y=300)


	self.grey_button=Button(master,text='Make grey image',width=20,command=grey_image,bg='grey')
	self.grey_button.pack()
	self.grey_button.place(x=10,y=590)
	#master.bind('<Key-s>',rgb)
