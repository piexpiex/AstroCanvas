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

def BIAS_IMAGES(self,master):
	#-------estimation of master bias image----------
	
	self.MASTER_BIAS_MAKER_text=Label(master,text='MASTER BIAS MAKER',width=45,bg='grey')
	self.MASTER_BIAS_MAKER_text.pack()
	self.MASTER_BIAS_MAKER_text.place(x=10,y=350)
	self.BIAS_text=Label(master,text='bias images',width=10,bg='grey')
	self.BIAS_text.pack()
	self.BIAS_text.place(x=10,y=380)
	self.BIAS_get=Entry(master,bg='grey',width=40)
	self.BIAS_get.insert(0,'bias.ls')
	self.BIAS_get.pack()
	self.BIAS_get.place(x=90,y=380)

	def read_image(image):
		image_name=str(image)
		if image_name[len(image_name)-5:]=='.fits':
			image_data=fits.open(image_name)[0].data
		else:
			print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS') 
		return(image_data)
	def delete_space(A):
		while A[0]==' ':
			A=A[1:len(A)]
		while A[len(A)-1]==' ':
			A=A[0:len(A)-1]
		return(A)
	def read_list(file_list):
		image_list=[]
		fichero=open(file_list)
		for linea in fichero:
			linea=linea[0:len(linea)-1]
			image_list.append(delete_space(linea))
		return(image_list)
	def bias_image(*event):
		BIAS_list=self.BIAS_get.get()
		BIAS_images=read_list(BIAS_list)
		for j in range(len(BIAS_images)):
			if j==0:
				BIAS_data=np.array(read_image(BIAS_images[j]))
			else:
				BIAS_data=np.dstack((BIAS_data,np.array(read_image(BIAS_images[j]))))

		BIAS_x_1,BIAS_x_2,BIAS_y_1,BIAS_y_2=0,0,0,0
		#Selection of combining method
		combining_method=combining.get()
		
		if combining_method=='average':
			MASTER_BIAS=np.mean(BIAS_data,axis=2)
			print(np.shape(MASTER_BIAS))
			MASTER_BIAS_std=np.std(BIAS_data,axis=2)
			print(np.shape(MASTER_BIAS_std))
		elif combining_method=='median':
			MASTER_BIAS=np.median(BIAS_data,axis=2)
			print(np.shape(MASTER_BIAS))
		elif combining_method=='1 sigma clipping':
			MASTER_BIAS=0
		elif combining_method=='2 sigma clipping':
			MASTER_BIAS=0
		elif combining_method=='3 sigma clipping':
			MASTER_BIAS=0

		#Normalization of each image and plotting
		#r=r[r_x_1:r_x_2,r_y_1:r_y_2]
		#grey_max=max(np.amax(grey,axis=0))
		#grey=grey/grey_max
	
		fig, ax = plt.subplots()
		axoff_fun(ax)

		im = ax.imshow(MASTER_BIAS,vmin=np.mean(MASTER_BIAS)-np.std(MASTER_BIAS),vmax=np.mean(MASTER_BIAS)+np.std(MASTER_BIAS), interpolation='nearest', origin='lower', cmap='gray',aspect='auto')
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
	


	combining = StringVar(master)
	combining.set("average") # initial value

	self.combining_text=Label(master,text='Combining method',width=20,bg='grey')
	self.combining_text.pack()
	self.combining_text.place(x=10,y=300,height=30)
	self.combining_get = OptionMenu(master, combining, 'average', 'median','1 sigma clipping','2 sigma clipping','3 sigma clipping')
	self.combining_get.config(width=10,bg='grey',highlightthickness=0)
	self.combining_get.pack()
	self.combining_get.place(x=200,y=300,height=30)
	
	self.combining_button=Button(master,text='Make master bias',width=20,command=bias_image,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)

	#master.bind('<Key-s>',rgb)
