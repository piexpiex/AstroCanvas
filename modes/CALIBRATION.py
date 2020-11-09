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

def CALIBRATION_IMAGES(self,master):
	#-------Calibration of astronomical images----------
	
	
	self.IMAGE_MAKER_text=Label(master,text='IMAGE CALIBRATION',width=45,bg='grey')
	self.IMAGE_MAKER_text.pack()
	self.IMAGE_MAKER_text.place(x=10,y=350)
	self.IMAGE_text=Label(master,text='images',width=10,bg='grey')
	self.IMAGE_text.pack()
	self.IMAGE_text.place(x=10,y=380)
	self.IMAGE_get=Entry(master,bg='grey',width=40)
	self.IMAGE_get.insert(0,'images.ls')
	self.IMAGE_get.pack()
	self.IMAGE_get.place(x=90,y=380)
	
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
	self.MASTER_BIAS_get.insert(0,'bias.fits')
	self.MASTER_BIAS_get.pack()
	self.MASTER_BIAS_get.place(x=90,y=440)
	
	self.MASTER_DARK_text=Label(master,text='master dark',width=10,bg='grey')
	self.MASTER_DARK_text.pack()
	self.MASTER_DARK_text.place(x=10,y=470)
	self.MASTER_DARK_get=Entry(master,bg='grey',width=40)
	self.MASTER_DARK_get.insert(0,'dark.fits')
	self.MASTER_DARK_get.pack()
	self.MASTER_DARK_get.place(x=90,y=470)
	
	self.MASTER_FLAT_text=Label(master,text='master flat',width=10,bg='grey')
	self.MASTER_FLAT_text.pack()
	self.MASTER_FLAT_text.place(x=10,y=500)
	self.MASTER_FLAT_get=Entry(master,bg='grey',width=40)
	self.MASTER_FLAT_get.insert(0,'flat.fits')
	self.MASTER_FLAT_get.pack()
	self.MASTER_FLAT_get.place(x=90,y=500)

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
		print(keyword)
		if keyword=='auto':
			image_list=[]
			time_list=[]
			fichero=open(file_list)
			post_linea=''
			for linea in fichero:
				medidor=0
				post_linea='0 '
				print(len(linea))
				for k in range(len(linea)-2):
					print(k)
					if medidor==0:
						if linea[k]==' ':
							post_linea=linea[k:]
							linea=linea[0:k]
							medidor=1
					else:
						continue
				tiempo=post_linea[0:len(post_linea)-1]
				print('tiempo',tiempo)
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
	def cal_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
		global MASTER_IMAGE
		global MASTER_IMAGE_std
		global MIN_MASTER_IMAGE_std
		global MAX_MASTER_IMAGE_std
		
		image_list=self.IMAGE_get.get()
		time_keyword=self.time_get.get()
		BIAS=self.MASTER_BIAS_get.get()
		BIAS_MASTER=np.array(read_image(BIAS))
		DARK=self.MASTER_DARK_get.get()
		try:
			DARK_MASTER=np.array(read_image(DARK,warning_no='no'))
		except:
			DARK_MASTER=np.zeros(np.shape(BIAS_MASTER))
		FLAT=self.MASTER_FLAT_get.get()
		FLAT_MASTER=np.array(read_image(FLAT))
		if time_keyword=='auto' or time_keyword=='AUTO':
			cal_images,time_list=read_list(image_list,keyword='auto')
		else:
			cal_images,time_list=read_list(image_list,keyword=time_keyword)
		print(time_list)
		for j in range(len(cal_images)):
			if j==0:
				cal_data=((np.array(read_image(cal_images[j])) - BIAS_MASTER)/time_list[j] - DARK_MASTER)/5
			else:
				cal_data=np.dstack((cal_data,((np.array(read_image(cal_images[j])) - BIAS_MASTER  )/time_list[j] - DARK_MASTER)/5)  )

		#Cut image
		cal_x_1,cal_x_2,cal_y_1,cal_y_2=self.Ymin_value.get(),self.Ymax_value.get(),self.Xmin_value.get(),self.Xmax_value.get()
		#Selection of combining method
		combining_method=combining.get()
		
		if combining_method=='average':
			MASTER_IMAGE=np.mean(cal_data,axis=2)
			print(np.shape(MASTER_IMAGE))
			MASTER_IMAGE_std=np.std(cal_data,axis=2)
			print(MASTER_IMAGE)
		elif combining_method=='median':
			MASTER_IMAGE=np.median(cal_data,axis=2)
			print(np.shape(MASTER_IMAGE))
			MASTER_IMAGE_std=np.std(cal_data,axis=2)
			print(MASTER_IMAGE)
		MAX_MASTER_IMAGE=max(np.amax(MASTER_IMAGE,axis=0))
		MIN_MASTER_IMAGE=min(np.amin(MASTER_IMAGE,axis=0))
		MAX_MASTER_IMAGE_std=max(np.amax(MASTER_IMAGE_std,axis=0))
		MIN_MASTER_IMAGE_std=min(np.amin(MASTER_IMAGE_std,axis=0))
		try:
			MASTER_IMAGE=MASTER_IMAGE[int(cal_x_1):int(cal_x_2),int(cal_y_1):int(cal_y_2)]
			MASTER_IMAGE_std=MASTER_IMAGE_std[int(cal_x_1):int(cal_x_2),int(cal_y_1):int(cal_y_2)]
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
	
		#toolbar = NavigationToolbar2Tk(canvas, master)
		#toolbar.update()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas.get_tk_widget().place(x=400,y=150)
		#plt.show()
		
	def cal_std(*event):
		#destroy previous canvas to save memory
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
	
	self.combining_button=Button(master,text='Make image',width=20,command=cal_image,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)
	
	self.show_std_button=Button(master,text='Show standard deviation',width=20,command=cal_std,bg='grey')
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

