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
	self.qa_get=Scale(master,from_=0,orient=HORIZONTAL,to=100,resolution=1,width=10,sliderlength=10,length=200,bg='grey')
	self.qa_get.pack()
	self.qa_get.place(x=100,y=350)
	self.st_text=Label(master,text='Strength',width=10,bg='grey')
	self.st_text.pack()
	self.st_text.place(x=10,y=400)
	self.st_get=Scale(master,from_=1,orient=HORIZONTAL,to=100,resolution=0.1,width=10,sliderlength=10,length=200,bg='grey') #orient=HORIZONTAL,
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
		try:
			image=float(image)
		except:
			pass
		if type(image)==str:
			image_name=str(image)
			if image_name[len(image_name)-5:]=='.fits':
				image_data=fits.open(image_name)[0].data
			else:
				print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS') 
		else:
			image_data=image
		return(image_data)


	def grey_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
			
		grey=self.grey_get.get()
		
		grey=read_image(grey)
		st=1/self.st_get.get()
		st_float=float(st)
		
		qa=self.qa_get.get()
		qa_float=float(qa)

		#Selection of scale
		Scale=scale.get() #Scale=input('Scale')
		if Scale=='linear':
			pass
		elif Scale=='logaritmic':
			grey=np.log10(grey+1)

		
		#Cut image
		g_x_1,g_x_2,g_y_1,g_y_2=self.Ymin_value.get(),self.Ymax_value.get(),self.Xmin_value.get(),self.Xmax_value.get()
		try:
			grey=grey[int(g_x_1):int(g_x_2),int(g_y_1):int(g_y_2)]
		except:
			pass
		#Normalization of each image and plotting
		grey_max=max(np.amax(grey,axis=0))
		grey=grey/grey_max
		
		rgb = make_lupton_rgb(grey,grey,grey,minimum=0, Q=qa_float, stretch=st_float) #, filename="imagen_rgb.jpeg"
		fig, ax = plt.subplots()
		axoff_fun(ax)
		im = ax.imshow(rgb, interpolation='nearest', cmap='gray', origin='lower')
		fig.set_size_inches(4.5,4.5)
		
		self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	
		toolbar = NavigationToolbar2Tk(self.canvas, master)
		toolbar.update()
		
		self.canvas.toolbar.place(x=900,y=430)
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		#plt.show()
		
		
		
		#display information
		print('\n \n Grey image')
		print('------------')
		print('average= (', np.mean(grey),')')
		print('standard deviation= (', np.std(grey),')')
		print('max= (', max(np.amax(grey,axis=0)),')')
		print('min= (', min(np.amin(grey,axis=0)),')')
		print('size=',np.shape(grey)[0],'X',np.shape(grey)[1])

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
	self.canvas.get_tk_widget().place(x=400,y=150)
	
	toolbar = NavigationToolbar2Tk(self.canvas, master)
	toolbar.update()
		
	self.canvas.toolbar.place(x=900,y=430)
	self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	self.canvas.get_tk_widget().place(x=400,y=150)
	self.toolbar_text=Label(master,text='Toolbar',width=40,bg='grey')
	self.toolbar_text.pack()
	self.toolbar_text.place(x=900,y=400)
	
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
	self.image_name.insert(0,'insert name')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)

	self.grey_button=Button(master,text='Make grey image',width=20,command=grey_image,bg='grey')
	self.grey_button.pack()
	self.grey_button.place(x=10,y=590)
	#master.bind('<Key-s>',rgb)
	
	self.ZOOM_text=Label(master,text='Crop image',width=40,bg='grey')
	self.ZOOM_text.pack()
	self.ZOOM_text.place(x=900,y=470)
	
	self.Xmin_text=Label(master,text='X min',bg='grey')
	self.Xmin_text.pack()
	self.Xmin_text.place(x=900,y=500,width=60,height=30)
	self.Xmin_value=Entry(master,bg='grey')
	self.Xmin_value.insert(0,'')
	self.Xmin_value.pack()
	self.Xmin_value.place(x=975,y=500,width=60,height=30)
	
	self.Xmax_text=Label(master,text='X max',bg='grey')
	self.Xmax_text.pack()
	self.Xmax_text.place(x=1050,y=500,width=60,height=30)
	self.Xmax_value=Entry(master,bg='grey')
	self.Xmax_value.insert(0,'')
	self.Xmax_value.pack()
	self.Xmax_value.place(x=1125,y=500,width=60,height=30)
	
	self.Ymin_text=Label(master,text='Y min',bg='grey')
	self.Ymin_text.pack()
	self.Ymin_text.place(x=900,y=550,width=60,height=30)
	self.Ymin_value=Entry(master,bg='grey')
	self.Ymin_value.insert(0,'')
	self.Ymin_value.pack()
	self.Ymin_value.place(x=975,y=550,width=60,height=30)
	
	self.Ymax_text=Label(master,text='Y max',bg='grey')
	self.Ymax_text.pack()
	self.Ymax_text.place(x=1050,y=550,width=60,height=30)
	self.Ymax_value=Entry(master,bg='grey')
	self.Ymax_value.insert(0,'')
	self.Ymax_value.pack()
	self.Ymax_value.place(x=1125,y=550,width=60,height=30)
