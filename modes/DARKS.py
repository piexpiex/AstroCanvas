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

def DARK_IMAGES(self,master):
	#-------estimation of master DARK image----------
	
	
	self.MASTER_DARK_MAKER_text=Label(master,text='MASTER DARK MAKER',width=45,bg='grey')
	self.MASTER_DARK_MAKER_text.pack()
	self.MASTER_DARK_MAKER_text.place(x=10,y=350)
	self.DARK_text=Label(master,text='dark images',width=10,bg='grey')
	self.DARK_text.pack()
	self.DARK_text.place(x=10,y=380)
	self.DARK_get=Entry(master,bg='grey',width=40)
	self.DARK_get.insert(0,'dark.ls')
	self.DARK_get.pack()
	self.DARK_get.place(x=90,y=380)
	
	self.time_text=Label(master,text='time keyword',width=10,bg='grey')
	self.time_text.pack()
	self.time_text.place(x=10,y=410)
	self.time_get=Entry(master,bg='grey',width=40)
	self.time_get.insert(0,'AUTO')
	self.time_get.pack()
	self.time_get.place(x=90,y=410)
	
	self.MASTER_BIAS_text=Label(master,text='master bias',width=10,bg='grey')
	self.MASTER_BIAS_text.pack()
	self.MASTER_BIAS_text.place(x=10,y=440)
	self.MASTER_BIAS_get=Entry(master,bg='grey',width=40)
	self.MASTER_BIAS_get.insert(0,'BIAS.fits')
	self.MASTER_BIAS_get.pack()
	self.MASTER_BIAS_get.place(x=90,y=440)

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
				try:
					fichero=open(image)
					for linea in fichero:
						image_name=linea
						break
					image_data=fits.open(image_name[0:len(image_name)-1])[0].data
				except:
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
	def read_list(file_list,keyword):
		if file_list[len(file_list)-4:]=='fits':
			image_list=[file_list]
			hdul = fits.open(file_list)
			hdr = hdul[0].header
			try:
				tiempo=float(keyword)
				time_list=[tiempo]
			except:
				tiempo=hdr[keyword]
				time_list=[tiempo]
			return(image_list,time_list)
		elif keyword=='auto':
			image_list=[]
			time_list=[]
			fichero=open(file_list)
			post_linea=''
			for linea in fichero:
				medidor=0
				post_linea='0 '
				for k in range(len(linea)-2):
					if medidor==0:
						if linea[k]==' ':
							post_linea=linea[k:]
							linea=linea[0:k]
							medidor=1
					else:
						continue
				tiempo=post_linea[0:len(post_linea)-1]
				image_list.append(delete_space(linea))
				time_list.append(float(delete_space(tiempo)))
			return(image_list,time_list)
		else:
			image_list=[]
			time_list=[]
			fichero=open(file_list)
			for linea in fichero:
				linea=linea[0:len(linea)-1]
				image_list.append(delete_space(linea))
			try:
				tiempo=float(keyword)
				time_list=[tiempo]
			except:
				for image in image_list:
					hdul = fits.open(image)
					hdr = hdul[0].header
					tiempo=hdr[keyword]
					time_list.append(float(tiempo))
			return(image_list,time_list)
	def dark_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
		global MASTER_DARK
		global MASTER_DARK_std
		global MIN_MASTER_DARK_std
		global MAX_MASTER_DARK_std
		
		DARK_list=self.DARK_get.get()
		time_keyword=self.time_get.get()
		BIAS=self.MASTER_BIAS_get.get()
		BIAS_MASTER=np.array(read_image(BIAS))
		if time_keyword=='auto' or time_keyword=='AUTO':
			DARK_images,time_list=read_list(DARK_list,keyword='auto')
		else:
			DARK_images,time_list=read_list(DARK_list,keyword=time_keyword)
		for j in range(len(DARK_images)):
			if j==0:
				DARK_data=(np.array(read_image(DARK_images[j])) - BIAS_MASTER)/time_list[j]
			else:
				DARK_data=np.dstack((DARK_data,(np.array(read_image(DARK_images[j])) - BIAS_MASTER)/time_list[j]))

		#Cut image
		DARK_x_1,DARK_x_2,DARK_y_1,DARK_y_2=self.Ymin_value.get(),self.Ymax_value.get(),self.Xmin_value.get(),self.Xmax_value.get()
		#Selection of combining method
		combining_method=combining.get()
		
		if len(DARK_images)>1:
			if combining_method=='average':
				MASTER_DARK=np.mean(DARK_data,axis=2)
				MASTER_DARK_std=np.std(DARK_data,axis=2)
			elif combining_method=='median':
				MASTER_DARK=np.median(DARK_data,axis=2)
				MASTER_DARK_std=np.std(DARK_data,axis=2)
		else:
			MASTER_DARK=DARK_data
			MASTER_DARK_std=np.zeros((10,10))
			print('only one dark image has been founded')
			
		MAX_MASTER_DARK=max(np.amax(MASTER_DARK,axis=0))
		MIN_MASTER_DARK=min(np.amin(MASTER_DARK,axis=0))
		MAX_MASTER_DARK_std=max(np.amax(MASTER_DARK_std,axis=0))
		MIN_MASTER_DARK_std=min(np.amin(MASTER_DARK_std,axis=0))
		try:
			MASTER_DARK=MASTER_DARK[int(DARK_x_1):int(DARK_x_2),int(DARK_y_1):int(DARK_y_2)]
			MASTER_DARK_std=MASTER_DARK_std[int(DARK_x_1):int(DARK_x_2),int(DARK_y_1):int(DARK_y_2)]
		except:
			pass
	
		y, x = np.mgrid[slice(0,len(MASTER_DARK[:,0])+1, 1) ,slice(0, len(MASTER_DARK[0,:])+1, 1) ]
		cmap = plt.get_cmap('hot')
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		
		im = ax.pcolormesh(x, y, MASTER_DARK, cmap=cmap)
		im.set_clim(MIN_MASTER_DARK, MAX_MASTER_DARK)
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
		try:
			plt.close(fig)
		except:
			pass
		#plt.show()
		
		#display information
		print('\n \n Dark image')
		print('------------')
		print('average= (', np.mean(MASTER_DARK),')')
		print('standard deviation= (', np.std(MASTER_DARK),')')
		print('max= (', max(np.amax(MASTER_DARK,axis=0)),')')
		print('min= (', min(np.amin(MASTER_DARK,axis=0)),')')
		print('size=',np.shape(MASTER_DARK)[0],'X',np.shape(MASTER_DARK)[1])
		
	def dark_std(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
			
		global MASTER_DARK_std
		global MIN_MASTER_DARK_std
		global MAX_MASTER_DARK_std
		
		y, x = np.mgrid[slice(0,len(MASTER_DARK_std[:,0])+1, 1) ,slice(0, len(MASTER_DARK_std[0,:])+1, 1) ]
		cmap = plt.get_cmap('hot')
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		
		im = ax.pcolormesh(x, y, MASTER_DARK_std, cmap=cmap)
		im.set_clim(MIN_MASTER_DARK_std, MAX_MASTER_DARK_std)
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
		try:
			plt.close(fig)
		except:
			pass
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
	try:
		plt.close(fig)
	except:
		pass
	self.toolbar_text=Label(master,text='Toolbar',width=40,bg='grey')
	self.toolbar_text.pack()
	self.toolbar_text.place(x=900,y=400)

	combining = StringVar(master)
	combining.set("average") # initial value

	self.combining_text=Label(master,text='Combining images',width=20,bg='grey')
	self.combining_text.pack()
	self.combining_text.place(x=10,y=300,height=30)
	self.combining_get = OptionMenu(master, combining, 'average', 'median')
	self.combining_get.config(width=10,bg='grey',highlightthickness=0)
	self.combining_get.pack()
	self.combining_get.place(x=200,y=300,height=30)
	
	def save_image(*event):
		global MASTER_DARK
		name=self.image_name.get()
		hdu = fits.PrimaryHDU(MASTER_DARK)
		t = fits.HDUList([hdu])
		t.writeto(name+'.fits',overwrite=True)
	
	self.save_image_text=Button(master,text='Save master dark as',width=20,bg='grey',command=save_image)
	self.save_image_text.pack()
	self.save_image_text.place(x=400,y=620)
	self.image_name=Entry(master,bg='grey')
	self.image_name.insert(0,'insert name')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)
	
	self.combining_button=Button(master,text='Make master dark',width=20,command=dark_image,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)
	
	self.show_std_button=Button(master,text='Show standard deviation',width=20,command=dark_std,bg='grey')
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

