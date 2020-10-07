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


def RGB_IMAGES(self,master):
	#-------Imagen RGB----------

	#Selection contrast and Stretch
	#qa=100
	#st=1
	self.qa_text=Label(master,text='Contrast',width=10,bg='grey')
	self.qa_text.pack()
	self.qa_text.place(x=10,y=350)
	self.qa_get=Scale(master,from_=0,orient=HORIZONTAL,to=1000,resolution=10,width=10,sliderlength=10,length=200,bg='grey')
	self.qa_get.pack()
	self.qa_get.place(x=100,y=350)
	self.st_text=Label(master,text='Strength',width=10,bg='grey')
	self.st_text.pack()
	self.st_text.place(x=10,y=400)
	self.st_get=Scale(master,from_=1,orient=HORIZONTAL,to=100,resolution=0.1,width=10,sliderlength=10,length=200,bg='grey') #orient=HORIZONTAL,
	self.st_get.pack()
	self.st_get.place(x=100,y=400)
	#Selection of images
	#r=fits.open('Filter_i-0-.fits')[0].data
	#g=fits.open('Filter_i-0-.fits')[0].data
	#b=fits.open('Filter_i-0-.fits')[0].data
	
	self.RGB_MAKER_text=Label(master,text='RGB MAKER',width=45,bg='grey')
	self.RGB_MAKER_text.pack()
	self.RGB_MAKER_text.place(x=10,y=470)
	self.red_text=Label(master,text='red image',width=10,bg='grey')
	self.red_text.pack()
	self.red_text.place(x=10,y=500)
	self.r_get=Entry(master,bg='red',width=40)
	self.r_get.insert(0,'Filter_i-0-.fits')
	self.r_get.pack()
	self.r_get.place(x=90,y=500)
	self.green_text=Label(master,text='green image',width=10,bg='grey')
	self.green_text.pack()
	self.green_text.place(x=10,y=530)
	self.g_get=Entry(master,bg='green',width=40)
	self.g_get.insert(0,'Filter_i-0-.fits')
	self.g_get.pack()
	self.g_get.place(x=90,y=530)
	self.blue_text=Label(master,text='blue image',width=10,bg='grey')
	self.blue_text.pack()
	self.blue_text.place(x=10,y=560)
	self.b_get=Entry(master,bg='blue',width=40)
	self.b_get.insert(0,'Filter_i-0-.fits')
	self.b_get.pack()
	self.b_get.place(x=90,y=560)
	def rgb(*event):
		print('a')
	self.FIT_IMAGES_text=Label(master,text='Fit images',width=40,bg='grey')
	self.FIT_IMAGES_text.pack()
	self.FIT_IMAGES_text.place(x=900,y=200)
	self.red_left_button=Button(master,text='<--',width=10,command=rgb,bg='red')
	self.red_left_button.pack()
	self.red_left_button.place(x=900,y=230)
	self.red_up_button=Button(master,text='B',width=10,command=rgb,bg='red')
	self.red_up_button.pack()
	self.red_up_button.place(x=910,y=230)
	self.red_right_button=Button(master,text='-->',width=10,command=rgb,bg='red')
	self.red_right_button.pack()
	self.red_right_button.place(x=920,y=230)
	self.red_down_button=Button(master,text='A',width=10,command=rgb,bg='red')
	self.red_down_button.pack()
	self.red_down_button.place(x=980,y=230)
	self.green_left_button=Button(master,text='<--',width=10,command=rgb,bg='green')
	self.green_left_button.pack()
	self.green_left_button.place(x=900,y=260)
	self.green_up_button=Button(master,text='B',width=10,command=rgb,bg='green')
	self.green_up_button.pack()
	self.green_up_button.place(x=910,y=260)
	self.green_right_button=Button(master,text='-->',width=10,command=rgb,bg='green')
	self.green_right_button.pack()
	self.green_right_button.place(x=920,y=260)
	self.green_down_button=Button(master,text='A',width=10,command=rgb,bg='green')
	self.green_down_button.pack()
	self.green_down_button.place(x=930,y=260)
	self.blue_left_button=Button(master,text='<--',width=10,command=rgb,bg='blue')
	self.blue_left_button.pack()
	self.blue_left_button.place(x=900,y=290)
	self.blue_up_button=Button(master,text='B',width=10,command=rgb,bg='blue')
	self.blue_up_button.pack()
	self.blue_up_button.place(x=910,y=290)
	self.blue_right_button=Button(master,text='-->',width=10,command=rgb,bg='blue')
	self.blue_right_button.pack()
	self.blue_right_button.place(x=920,y=290)
	self.blue_down_button=Button(master,text='A',width=10,command=rgb,bg='blue')
	self.blue_down_button.pack()
	self.blue_down_button.place(x=930,y=290)
	
	self.AUTO_FIT_button=Button(master,text='Auto fit',width=30,command=rgb,bg='grey')
	self.AUTO_FIT_button.pack()
	self.AUTO_FIT_button.place(x=900,y=330)
	
	self.ZOOM_text=Label(master,text='Image zoom',width=40,bg='grey')
	self.ZOOM_text.pack()
	self.ZOOM_text.place(x=900,y=470)
	self.mas_button=Button(master,text='mas',width=20,command=rgb,bg='grey')
	self.mas_button.pack()
	self.mas_button.place(x=900,y=500)
	self.menos_button=Button(master,text='menos',width=20,command=rgb,bg='grey')
	self.menos_button.pack()
	self.menos_button.place(x=950,y=500)

	def read_image(image):
		image_name=str(image)
		if image_name[len(image_name)-5:]=='.fits':
			image_data=fits.open(image_name)[0].data
		else:
			print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS') 
		return(image_data)


	def rgb(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
			
		r=self.r_get.get()
		g=self.g_get.get()
		b=self.b_get.get()
		r=read_image(r)
		g=read_image(g)
		b=read_image(b)
		st=1/self.st_get.get()
		st_float=float(st)
		
		qa=self.qa_get.get()
		qa_float=float(qa)
		r=r[200:900,300:1000]
		g=g[100:800,300:1000]
		b=b[200:900,200:900]
		#Identification of sources for a good overlap
	

		r_x_1,r_x_2,r_y_1,r_y_2=0,0,0,0
		g_x_1,g_x_2,g_y_1,g_y_2=0,0,0,0
		b_x_1,b_x_2,b_y_1,b_y_2=0,0,0,0
		#Selection of scale
		Scale=scale.get() #Scale=input('Scale')
		if Scale=='linear':
			pass
		elif Scale=='logaritmic':
			r=np.log10(r+1)
			g=np.log10(g+1)
			b=np.log10(b+1)

		#Normalization of each image and plotting
		#r=r[r_x_1:r_x_2,r_y_1:r_y_2]
		r_max=max(np.amax(r,axis=0))
		r=r/r_max
		
		#g=g[g_x_1:g_x_2,g_y_1:g_y_2]
		g_max=max(np.amax(g,axis=0))
		g=g/g_max
		
		#b=b[b_x_1:b_x_2,b_y_1:b_y_2]
		b_max=max(np.amax(b,axis=0))
		b=b/b_max
	
		rgb = make_lupton_rgb(r,g,b,minimum=0, Q=qa_float, stretch=st_float) #, filename="imagen_rgb.jpeg"
		fig, ax = plt.subplots()
		axoff_fun(ax)
		im = ax.imshow(rgb, interpolation='nearest', cmap='gray', origin='lower')
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
	#self.canvas.draw()
	self.canvas.get_tk_widget().pack()
	#self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	#toolbar = NavigationToolbar2Tk(canvas, master)
	#toolbar.update()
	#self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	self.canvas.get_tk_widget().place(x=400,y=150)
	
	#if self.image_name.get()!='insert name and Make a rgb image':
	def save_image(*event):
		name=self.image_name.get()
		plt.savefig(name+'.png')


	scale = StringVar(master)
	scale.set("linear") # initial value

	self.Scale_text=Label(master,text='Scale',width=10,bg='grey')
	self.Scale_text.pack()
	self.Scale_text.place(x=10,y=300)
	self.Scale_get = OptionMenu(master, scale, 'logaritmic', 'linear')
	self.Scale_get.config(width=10,bg='grey',highlightthickness=0)
	self.Scale_get.pack()
	self.Scale_get.place(x=100,y=300)
	
	self.save_image_text=Button(master,text='Save image as',width=20,bg='grey',command=save_image)
	self.save_image_text.pack()
	self.save_image_text.place(x=400,y=620)
	self.image_name=Entry(master,bg='grey')
	self.image_name.insert(0,'insert name and Make a rgb image')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)


	self.rgb_button=Button(master,text='Make rgb image',width=20,command=rgb,bg='grey')
	self.rgb_button.pack()
	self.rgb_button.place(x=10,y=590)
	#master.bind('<Key-s>',rgb)
