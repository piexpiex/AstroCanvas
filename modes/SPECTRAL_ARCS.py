import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from tkinter import *
import sys
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def SPECTRAL_ARCS(self,master):
	#-------Calibration of astronomical images----------
	
	self.FIT_IMAGES_text=Label(master,text='Fit images',width=40,bg='grey')
	self.FIT_IMAGES_text.pack()
	self.FIT_IMAGES_text.place(x=900,y=200)
	self.turn_text=Label(master,text='turn image',bg='grey')
	self.turn_text.pack()
	self.turn_text.place(x=900,y=230,width=70,height=22)
	self.turn_get=Entry(master,bg='grey')
	self.turn_get.insert(0,'')
	self.turn_get.pack()
	self.turn_get.place(x=975,y=230,width=210,height=22)
	
	function_model = StringVar(master)
	function_model.set("gaussian") # initial value
	self.function_model_text=Label(master,text='function',bg='grey')
	self.function_model_text.pack()
	self.function_model_text.place(x=900,y=260,width=70,height=22)
	self.function_model_get = OptionMenu(master, function_model,'gaussian','voigt','lorentz')
	self.function_model_get.config(bg='grey',highlightthickness=0)
	self.function_model_get.pack()
	self.function_model_get.place(x=975,y=260,width=210,height=22)
	
	self.IMAGE_MAKER_text=Label(master,text='SPECTRAL ARCS',width=45,bg='grey')
	self.IMAGE_MAKER_text.pack()
	self.IMAGE_MAKER_text.place(x=10,y=350)
	self.IMAGE_text=Label(master,text='images',width=10,bg='grey')
	self.IMAGE_text.pack()
	self.IMAGE_text.place(x=10,y=380)
	self.IMAGE_get=Entry(master,bg='grey',width=40)
	self.IMAGE_get.insert(0,'arcos.ls')
	self.IMAGE_get.pack()
	self.IMAGE_get.place(x=90,y=380)

	def read_image(image):
		try:
			image=float(image)
		except:
			pass
		if type(image)==str:
			image_name=delete_space(str(image))
			if image_name[len(image_name)-5:]=='.fits':
				image_data=fits.open(image_name)[0].data
			else:
				print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS') 
		else:
			image_data=image
		return(image_data)
	def delete_space(A):
		if len(A)<2:
			pass
		else:
			while A[0]==' ' and len(A)>1:
				A=A[1:len(A)]
			while A[len(A)-1]==' ' and len(A)>1:
				A=A[0:len(A)-1]
		return(A)
	def read_list(file_list):
		if file_list[len(file_list)-4:]=='fits':
			image_list=[file_list]
		else:
			image_list=[]
			fichero=open(file_list)
			for linea in fichero:
				linea=linea[0:len(linea)-1]
				image_list.append(delete_space(linea))
		return(image_list)
	def arc_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
		global MASTER_IMAGE
		global MASTER_IMAGE_std
		global MIN_MASTER_IMAGE_std
		global MAX_MASTER_IMAGE_std
		
		image_list=self.IMAGE_get.get()
#################################################################################################
		arc_images=read_list(image_list)
		for j in range(len(arc_images)):
			if j==0:
				arc_data=np.array(read_image(arc_images[j])) #np.divide(((np.array(read_image(arc_images[j])) - BIAS_MASTER)/time_list[j] - DARK_MASTER),FLAT_MASTER)
			else:
				arc_data=np.dstack((arc_data,np.array(read_image(arc_images[j])))) #np.dstack((arc_data,np.divide(((np.array(read_image(arc_images[j])) - BIAS_MASTER  )/time_list[j] - DARK_MASTER),FLAT_MASTER))  )

		#Cut image
		arc_x_1,arc_x_2,arc_y_1,arc_y_2=self.Ymin_value.get(),self.Ymax_value.get(),self.Xmin_value.get(),self.Xmax_value.get()
		#Selection of combining method
		combining_method=combining.get()
		
		if len(arc_images)>1:
			if combining_method=='average':
				MASTER_IMAGE=np.mean(arc_data,axis=2)
				MASTER_IMAGE_std=np.std(arc_data,axis=2)
			elif combining_method=='median':
				MASTER_IMAGE=np.median(arc_data,axis=2)
				MASTER_IMAGE_std=np.std(arc_data,axis=2)
		else:
			MASTER_IMAGE=arc_data
			MASTER_IMAGE_std=np.zeros((10,10))
			print('only one spectral arc image has been founded')
				
		MAX_MASTER_IMAGE=max(np.amax(MASTER_IMAGE,axis=0))
		MIN_MASTER_IMAGE=min(np.amin(MASTER_IMAGE,axis=0))
		MAX_MASTER_IMAGE_std=max(np.amax(MASTER_IMAGE_std,axis=0))
		MIN_MASTER_IMAGE_std=min(np.amin(MASTER_IMAGE_std,axis=0))
		try:
			MASTER_IMAGE=MASTER_IMAGE[int(arc_x_1):int(arc_x_2),int(arc_y_1):int(arc_y_2)]
			MASTER_IMAGE_std=MASTER_IMAGE_std[int(arc_x_1):int(arc_x_2),int(arc_y_1):int(arc_y_2)]
		except:
			pass
	
		y, x = np.mgrid[slice(0,len(MASTER_IMAGE[:,0])+1, 1) ,slice(0, len(MASTER_IMAGE[0,:])+1, 1) ]
		cmap = plt.get_cmap('hot')
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		
		im = ax.pcolormesh(x, y, MASTER_IMAGE, cmap=cmap)
		im.set_clim(MIN_MASTER_IMAGE, MAX_MASTER_IMAGE)
		fig.colorbar(im, ax=ax)

		fig.set_size_inches(4.5,4.5)
		
		self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	
		toolbar = NavigationToolbar2Tk(self.canvas, master)
		toolbar.update()
		
		self.canvas.toolbar.place(x=900,y=430)
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		#plt.show()
		
		#display information
		#print('\n \n Espectral lines')
		#print('------------')
		#print('average= (', np.mean(MASTER_BIAS),')')
		#print('standard deviation= (', np.std(MASTER_BIAS),')')
		#print('max= (', max(np.amax(MASTER_BIAS,axis=0)),')')
		#print('min= (', min(np.amin(MASTER_BIAS,axis=0)),')')
		#print('size=',np.shape(MASTER_DARK)[0],'X',np.shape(MASTER_DARK)[1])
		
	def arc_std(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
			
		global MASTER_IMAGE_std
		global MIN_MASTER_IMAGE_std
		global MAX_MASTER_IMAGE_std
		
		y, x = np.mgrid[slice(0,len(MASTER_IMAGE_std[:,0])+1, 1) ,slice(0, len(MASTER_IMAGE_std[0,:])+1, 1) ]
		cmap = plt.get_cmap('hot')
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		
		im = ax.pcolormesh(x, y, MASTER_IMAGE_std, cmap=cmap)
		im.set_clim(MIN_MASTER_IMAGE_std, MAX_MASTER_IMAGE_std)
		fig.colorbar(im, ax=ax)	
		fig.set_size_inches(4.5,4.5)
		
		#fig.savefig('test2png.png', dpi=100)
		self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	
		toolbar = NavigationToolbar2Tk(self.canvas, master)
		toolbar.update()
		
		self.canvas.toolbar.place(x=900,y=430)
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
	self.canvas.get_tk_widget().place(x=400,y=150)
	
	toolbar = NavigationToolbar2Tk(self.canvas, master)
	toolbar.update()
		
	self.canvas.toolbar.place(x=900,y=430)
	self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	self.canvas.get_tk_widget().place(x=400,y=150)
	self.toolbar_text=Label(master,text='Toolbar',width=40,bg='grey')
	self.toolbar_text.pack()
	self.toolbar_text.place(x=900,y=400)
	
	combining = StringVar(master)
	combining.set("average") # initial value

	self.combining_text=Label(master,text='Combining method',width=20,bg='grey')
	self.combining_text.pack()
	self.combining_text.place(x=10,y=300,height=30)
	self.combining_get = OptionMenu(master, combining, 'average', 'median')
	self.combining_get.config(width=10,bg='grey',highlightthickness=0)
	self.combining_get.pack()
	self.combining_get.place(x=200,y=300,height=30)
	
	def save_image(*event):
		global MASTER_IMAGE
		name=self.image_name.get()
		hdu = fits.PrimaryHDU(MASTER_IMAGE)
		t = fits.HDUList([hdu])
		t.writeto(name+'.fits',overwrite=True)
	
	self.save_image_text=Button(master,text='Save image as',width=20,bg='grey',command=save_image)
	self.save_image_text.pack()
	self.save_image_text.place(x=400,y=620)
	self.image_name=Entry(master,bg='grey')
	self.image_name.insert(0,'insert name')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)
	
	self.combining_button=Button(master,text='Make image',width=20,command=arc_image,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)
	
	self.show_std_button=Button(master,text='Show standard deviation',width=20,command=arc_std,bg='grey')
	self.show_std_button.pack()
	self.show_std_button.place(x=180,y=590)
	
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
