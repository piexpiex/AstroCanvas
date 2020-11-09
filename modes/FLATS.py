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

def FLAT_IMAGES(self,master):
	#-------estimation of master FLAT image----------
	
	
	self.MASTER_FLAT_MAKER_text=Label(master,text='MASTER FLAT MAKER',width=45,bg='grey')
	self.MASTER_FLAT_MAKER_text.pack()
	self.MASTER_FLAT_MAKER_text.place(x=10,y=350)
	self.FLAT_text=Label(master,text='flat images',width=10,bg='grey')
	self.FLAT_text.pack()
	self.FLAT_text.place(x=10,y=380)
	self.FLAT_get=Entry(master,bg='grey',width=40)
	self.FLAT_get.insert(0,'flats.ls')
	self.FLAT_get.pack()
	self.FLAT_get.place(x=90,y=380)
	
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
	
	self.MASTER_DARK_text=Label(master,text='master dark',width=10,bg='grey')
	self.MASTER_DARK_text.pack()
	self.MASTER_DARK_text.place(x=10,y=470)
	self.MASTER_DARK_get=Entry(master,bg='grey',width=40)
	self.MASTER_DARK_get.insert(0,'DARK.fits')
	self.MASTER_DARK_get.pack()
	self.MASTER_DARK_get.place(x=90,y=470)
	
	self.MASTER_NORMAL_text=Label(master,text='normalize',width=10,bg='grey')
	self.MASTER_NORMAL_text.pack()
	self.MASTER_NORMAL_text.place(x=10,y=500)
	self.MASTER_NORMAL_get=Entry(master,bg='grey',width=40)
	self.MASTER_NORMAL_get.insert(0,'yes')
	self.MASTER_NORMAL_get.pack()
	self.MASTER_NORMAL_get.place(x=90,y=500)

	def read_image(image,warning_no='yes'):
		image_name=str(image)
		if image_name[len(image_name)-5:]=='.fits':
			image_data=fits.open(image_name)[0].data
		else:
			if warning_no=='no':
				pass
			else:
				print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS') 
		return(image_data)
	def delete_space(A):
		if len(A)<2:
			pass
		else:
			while A[0]==' ' and len(A)>1:
				A=A[1:len(A)]
			while A[len(A)-1] and len(A)>1==' ':
				A=A[0:len(A)-1]
		return(A)
	def read_list(file_list,keyword):
		if keyword=='auto':
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
			for image in image_list:
				hdul = fits.open(image)
				hdr = hdul[0].header
				tiempo=hdr[keyword]
				time_list.append(float(tiempo))
			return(image_list,time_list)
	def flat_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
		global MASTER_FLAT
		global MASTER_FLAT_std
		global MIN_MASTER_FLAT_std
		global MAX_MASTER_FLAT_std
		
		FLAT_list=self.FLAT_get.get()
		time_keyword=self.time_get.get()
		BIAS=self.MASTER_BIAS_get.get()
		BIAS_MASTER=np.array(read_image(BIAS))
		DARK=self.MASTER_DARK_get.get()
		try:
			DARK_MASTER=np.array(read_image(DARK,warning_no='no'))
		except:
			DARK_MASTER=np.zeros(np.shape(BIAS_MASTER))
		NORMALIZE=self.MASTER_NORMAL_get.get()
		if time_keyword=='auto' or time_keyword=='AUTO':
			FLAT_images,time_list=read_list(FLAT_list,keyword='auto')
		else:
			FLAT_images,time_list=read_list(FLAT_list,keyword=time_keyword)
		for j in range(len(FLAT_images)):
			if j==0:
				FLAT_data=(np.array(read_image(FLAT_images[j])) - BIAS_MASTER)/time_list[j] - DARK_MASTER
			else:
				FLAT_data=np.dstack((FLAT_data,(np.array(read_image(FLAT_images[j])) - BIAS_MASTER  )/time_list[j] - DARK_MASTER))

		#Cut image
		FLAT_x_1,FLAT_x_2,FLAT_y_1,FLAT_y_2=self.Ymin_value.get(),self.Ymax_value.get(),self.Xmin_value.get(),self.Xmax_value.get()
		#Selection of combining method
		combining_method=combining.get()
		
		if combining_method=='average':
			MASTER_FLAT=np.mean(FLAT_data,axis=2)
			MASTER_FLAT_std=np.std(FLAT_data,axis=2)
		elif combining_method=='median':
			MASTER_FLAT=np.median(FLAT_data,axis=2)
			MASTER_FLAT_std=np.std(FLAT_data,axis=2)
			
		if NORMALIZE=='YES' or NORMALIZE=='yes':
			MASTER_FLAT_std=MASTER_FLAT_std/np.mean(MASTER_FLAT)
			MASTER_FLAT=MASTER_FLAT/np.mean(MASTER_FLAT)
			
		MAX_MASTER_FLAT=max(np.amax(MASTER_FLAT,axis=0))
		MIN_MASTER_FLAT=min(np.amin(MASTER_FLAT,axis=0))
		MAX_MASTER_FLAT_std=max(np.amax(MASTER_FLAT_std,axis=0))
		MIN_MASTER_FLAT_std=min(np.amin(MASTER_FLAT_std,axis=0))
		try:
			MASTER_FLAT=MASTER_FLAT[int(FLAT_x_1):int(FLAT_x_2),int(FLAT_y_1):int(FLAT_y_2)]
			MASTER_FLAT_std=MASTER_FLAT_std[int(FLAT_x_1):int(FLAT_x_2),int(FLAT_y_1):int(FLAT_y_2)]
		except:
			pass
	
		y, x = np.mgrid[slice(0,len(MASTER_FLAT[:,0])+1, 1) ,slice(0, len(MASTER_FLAT[0,:])+1, 1) ]
		cmap = plt.get_cmap('hot')
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		
		im = ax.pcolormesh(x, y, MASTER_FLAT, cmap=cmap)
		im.set_clim(MIN_MASTER_FLAT, MAX_MASTER_FLAT)
		fig.colorbar(im, ax=ax)

		fig.set_size_inches(4.5,4.5)
		
		self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	
		#toolbar = NavigationToolbar2Tk(canvas, master)
		#toolbar.update()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		#plt.show()
		
	def flat_std(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
			
		global MASTER_FLAT_std
		global MIN_MASTER_FLAT_std
		global MAX_MASTER_FLAT_std
		
		y, x = np.mgrid[slice(0,len(MASTER_FLAT_std[:,0])+1, 1) ,slice(0, len(MASTER_FLAT_std[0,:])+1, 1) ]
		cmap = plt.get_cmap('hot')
	
		fig, ax = plt.subplots()
		axoff_fun(ax)
		
		im = ax.pcolormesh(x, y, MASTER_FLAT_std, cmap=cmap)
		im.set_clim(MIN_MASTER_FLAT_std, MAX_MASTER_FLAT_std)
		fig.colorbar(im, ax=ax)	
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
	self.combining_get = OptionMenu(master, combining, 'average', 'median')
	self.combining_get.config(width=10,bg='grey',highlightthickness=0)
	self.combining_get.pack()
	self.combining_get.place(x=200,y=300,height=30)
	
	def save_image(*event):
		global MASTER_FLAT
		name=self.image_name.get()
		hdu = fits.PrimaryHDU(MASTER_FLAT)
		t = fits.HDUList([hdu])
		t.writeto(name+'.fits',overwrite=True)
	
	self.save_image_text=Button(master,text='Save master flat as',width=20,bg='grey',command=save_image)
	self.save_image_text.pack()
	self.save_image_text.place(x=400,y=620)
	self.image_name=Entry(master,bg='grey')
	self.image_name.insert(0,'insert name')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)
	
	self.combining_button=Button(master,text='Make master flat',width=20,command=flat_image,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)
	
	self.show_std_button=Button(master,text='Show standard deviation',width=20,command=flat_std,bg='grey')
	self.show_std_button.pack()
	self.show_std_button.place(x=180,y=590)
	
	self.ZOOM_text=Label(master,text='Image zoom',width=40,bg='grey')
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

