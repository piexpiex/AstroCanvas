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

	#Fit parameters
	
	#Selection contrast and Stretch
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
	
	#Selection of images
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
	
	#Fit images
	def rgb(*event):
		print('a')
	self.FIT_IMAGES_text=Label(master,text='Fit images',width=40,bg='grey')
	self.FIT_IMAGES_text.pack()
	self.FIT_IMAGES_text.place(x=900,y=200)
	
	
	self.red_X_text=Label(master,text='X min',bg='grey')
	self.red_X_text.pack()
	self.red_X_text.place(x=900,y=230,width=60,height=25)
	self.red_X_value=Entry(master,bg='grey')
	self.red_X_value.insert(0,'')
	self.red_X_value.pack()
	self.red_X_value.place(x=975,y=230,width=60,height=25)
	
	self.red_Y_text=Label(master,text='X max',bg='grey')
	self.red_Y_text.pack()
	self.red_Y_text.place(x=1050,y=230,width=60,height=25)
	self.red_Y_value=Entry(master,bg='grey')
	self.red_Y_value.insert(0,'')
	self.red_Y_value.pack()
	self.red_Y_value.place(x=1125,y=230,width=60,height=25)
	
	self.green_X_text=Label(master,text='X min',bg='grey')
	self.green_X_text.pack()
	self.green_X_text.place(x=900,y=260,width=60,height=25)
	self.green_X_value=Entry(master,bg='grey')
	self.green_X_value.insert(0,'')
	self.green_X_value.pack()
	self.green_X_value.place(x=975,y=260,width=60,height=25)
	
	self.green_Y_text=Label(master,text='X max',bg='grey')
	self.green_Y_text.pack()
	self.green_Y_text.place(x=1050,y=260,width=60,height=25)
	self.green_Y_value=Entry(master,bg='grey')
	self.green_Y_value.insert(0,'')
	self.green_Y_value.pack()
	self.green_Y_value.place(x=1125,y=260,width=60,height=25)
	
	self.blue_X_text=Label(master,text='X min',bg='grey')
	self.blue_X_text.pack()
	self.blue_X_text.place(x=900,y=290,width=60,height=25)
	self.blue_X_value=Entry(master,bg='grey')
	self.blue_X_value.insert(0,'')
	self.blue_X_value.pack()
	self.blue_X_value.place(x=975,y=290,width=60,height=25)
	
	self.blue_Y_text=Label(master,text='X max',bg='grey')
	self.blue_Y_text.pack()
	self.blue_Y_text.place(x=1050,y=290,width=60,height=25)
	self.blue_Y_value=Entry(master,bg='grey')
	self.blue_Y_value.insert(0,'')
	self.blue_Y_value.pack()
	self.blue_Y_value.place(x=1125,y=290,width=60,height=25)
	
	
	#Crop image
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
			_=self.canvas.toolbar.destroy()
		except:
			pass
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
		
		#esto es lo que habria que quitar########################################################################
		r=r[200:900,500:1000]
		g=g#[100:900,300:1000]
		b=b[200:900,200:900]
		
		
		autofit=str(self.AUTO_FIT_value.get())  #'no'
		
		#Manual fit
		if autofit!='yes':
			red_x_1,red_y_1=0,0
			green_x_1,green_y_1=0,0
			blue_x_1,blue_y_1=0,0
			try:
				red_x_1,red_y_1=int(self.red_Y_value.get()),int(self.red_X_value.get())
				green_x_1,green_y_1=int(self.green_Y_value.get()),int(self.green_X_value.get())
				blue_x_1,blue_y_1=int(self.blue_Y_value.get()),int(self.blue_X_value.get())
			except:
				pass
		
			base_x=min(red_x_1,green_x_1,blue_x_1)
			base_y=min(red_y_1,green_y_1,blue_y_1)
				
			red_x_1,green_x_1,blue_x_1=red_x_1-base_x,green_x_1-base_x,blue_x_1-base_x
			red_y_1,green_y_1,blue_y_1=red_y_1-base_y,green_y_1-base_y,blue_y_1-base_y
				
			max_x=max(np.shape(r)[0]+red_x_1,np.shape(g)[0]+green_x_1,np.shape(b)[0]+blue_x_1)
			max_y=max(np.shape(r)[1]+red_y_1,np.shape(g)[1]+green_y_1,np.shape(b)[1]+blue_y_1)
				
			r_copy=np.zeros((max_x,max_y))
			r_copy[red_x_1:red_x_1+np.shape(r)[0],red_y_1:red_y_1+np.shape(r)[1]]=r
			g_copy=np.zeros((max_x,max_y))
			g_copy[green_x_1:green_x_1+np.shape(g)[0],green_y_1:green_y_1+np.shape(g)[1]]=g
			b_copy=np.zeros((max_x,max_y))
			b_copy[blue_x_1:blue_x_1+np.shape(b)[0],blue_y_1:blue_y_1+np.shape(b)[1]]=b
			r=r_copy
			g=g_copy
			b=b_copy
			print('lkl')
			
		
		
		#AUTOFIT
		if autofit=='yes':
			y, x = np.mgrid[0:500,0:500]
			cd=plt.contour(x,y,r[0:500,0:500],np.array([24.8,25,25.4,25.8,26.2,27,28]),alpha=0.5) 
			print(cd)
			#identificación de los puntos en las imagenes para realizar el ajuste
			# los x e y van al reves en las matrices
			
			
			red_x_2,red_y_2=0,0
			green_x_2,green_y_2=0,0
			blue_x_2,blue_y_2=0,0
			
			self.red_X_value.delete(0,'end')
			self.red_Y_value.delete(0,'end')
			self.green_X_value.delete(0,'end')
			self.green_Y_value.delete(0,'end')
			self.blue_X_value.delete(0,'end')
			self.blue_Y_value.delete(0,'end')
			self.red_X_value.insert(0,str(red_x_2))
			self.red_Y_value.insert(0,str(red_y_2))
			self.green_X_value.insert(0,str(green_x_2))
			self.green_Y_value.insert(0,str(green_y_2))
			self.blue_X_value.insert(0,str(blue_x_2))
			self.blue_Y_value.insert(0,str(blue_y_2))
			
			base_x=min(red_x_2,green_x_2,blue_x_2)
			base_y=min(red_y_2,green_y_2,blue_y_2)
				
			red_x_2,green_x_2,blue_x_2=red_x_2-base_x,green_x_2-base_x,blue_x_2-base_x
			red_y_2,green_y_2,blue_y_2=red_y_2-base_y,green_y_2-base_y,blue_y_2-base_y
				
			max_x=max(np.shape(r)[0]+red_x_2,np.shape(g)[0]+green_x_2,np.shape(b)[0]+blue_x_2)
			max_y=max(np.shape(r)[1]+red_y_2,np.shape(g)[1]+green_y_2,np.shape(b)[1]+blue_y_2)
				
			r_copy=np.zeros((max_x,max_y))
			r_copy[red_x_2:red_x_2+np.shape(r)[0],red_y_2:red_y_2+np.shape(r)[1]]=r
			g_copy=np.zeros((max_x,max_y))
			g_copy[green_x_2:green_x_2+np.shape(g)[0],green_y_2:green_y_2+np.shape(g)[1]]=g
			b_copy=np.zeros((max_x,max_y))
			b_copy[blue_x_2:blue_x_2+np.shape(b)[0],blue_y_2:blue_y_2+np.shape(b)[1]]=b
			r=r_copy
			g=g_copy
			b=b_copy
				
		#Identification of sources for a good overlap
		
		#Selection of scale
		Scale=scale.get() #Scale=input('Scale')
		if Scale=='linear':
			pass
		elif Scale=='logaritmic':
			r=np.log10(r+1)
			g=np.log10(g+1)
			b=np.log10(b+1)

		#Cut image
		g_x_1,g_x_2,g_y_1,g_y_2=self.Ymin_value.get(),self.Ymax_value.get(),self.Xmin_value.get(),self.Xmax_value.get()
		try:
			r=r[int(g_x_1):int(g_x_2),int(g_y_1):int(g_y_2)]
			g=g[int(g_x_1):int(g_x_2),int(g_y_1):int(g_y_2)]
			b=b[int(g_x_1):int(g_x_2),int(g_y_1):int(g_y_2)]
		except:
			pass
			
		#Normalization of each image and plotting
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
		
		self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	
		toolbar = NavigationToolbar2Tk(self.canvas, master)
		toolbar.update()
		
		self.canvas.toolbar.place(x=900,y=430)
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		
		rgb_mean=np.mean(rgb,axis=2)
		
		#display information
		print('\n \n RGB image')
		print('------------')
		print('average= (', np.mean(rgb_mean),')')
		print('standard deviation= (', np.std(rgb_mean),')')
		print('max= (', max(np.amax(rgb_mean,axis=0)),')')
		print('min= (', min(np.amin(rgb_mean,axis=0)),')')
		print('size=',np.shape(rgb_mean)[0],'X',np.shape(rgb_mean)[1])

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
	self.image_name.insert(0,'insert name')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)
	
	self.AUTO_FIT_text=Label(master,text='Auto fit',bg='grey')
	self.AUTO_FIT_text.pack()
	self.AUTO_FIT_text.place(x=900,y=330,width=135,height=25)
	self.AUTO_FIT_value=Entry(master,bg='grey')
	self.AUTO_FIT_value.insert(0,'')
	self.AUTO_FIT_value.pack()
	self.AUTO_FIT_value.place(x=1050,y=330,width=135,height=25)
	
	
	
	self.rgb_button=Button(master,text='Make rgb image',width=20,command=rgb,bg='grey')
	self.rgb_button.pack()
	self.rgb_button.place(x=10,y=590)
	#master.bind('<Key-s>',rgb)
