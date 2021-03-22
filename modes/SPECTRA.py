import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from astropy.io import fits
from astropy.table import Table
from astropy.visualization import make_lupton_rgb
from tkinter import *
import sys
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from astropy.modeling import models, fitting

def SPECTRA(self,master):
	#-------visualization of spectra----------
	
	self.FIT_IMAGES_text=Label(master,text='Fit lines',width=40,bg='grey')
	self.FIT_IMAGES_text.pack()
	self.FIT_IMAGES_text.place(x=900,y=200)
	self.turn_text=Label(master,text='turn image',bg='grey')
	self.turn_text.pack()
	self.turn_text.place(x=900,y=200,width=70,height=22)
	self.turn_get=Entry(master,bg='grey')
	self.turn_get.insert(0,'')
	self.turn_get.pack()
	self.turn_get.place(x=975,y=200,width=210,height=22)
	
	function_model = StringVar(master)
	function_model.set("gaussian") # initial value
	self.function_model_text=Label(master,text='function',bg='grey')
	self.function_model_text.pack()
	self.function_model_text.place(x=900,y=228,width=70,height=22)
	self.function_model_get = OptionMenu(master, function_model,'gaussian','voigt','lorentz')
	self.function_model_get.config(bg='grey',highlightthickness=0)
	self.function_model_get.pack()
	self.function_model_get.place(x=975,y=228,width=210,height=22)
	
	self.background_text=Label(master,text='background',bg='grey')
	self.background_text.pack()
	self.background_text.place(x=900,y=256,width=70,height=22)
	self.background_get=Entry(master,bg='grey')
	self.background_get.insert(0,'')
	self.background_get.pack()
	self.background_get.place(x=975,y=256,width=210,height=22)
	
	self.mean_text=Label(master,text='mean',bg='grey')
	self.mean_text.pack()
	self.mean_text.place(x=900,y=284,width=70,height=22)
	self.mean_get=Entry(master,bg='grey')
	self.mean_get.insert(0,'')
	self.mean_get.pack()
	self.mean_get.place(x=975,y=284,width=210,height=22)
	
	self.intensity_text=Label(master,text='intensity',bg='grey')
	self.intensity_text.pack()
	self.intensity_text.place(x=900,y=312,width=70,height=22)
	self.intensity_get=Entry(master,bg='grey')
	self.intensity_get.insert(0,'')
	self.intensity_get.pack()
	self.intensity_get.place(x=975,y=312,width=210,height=22)
	
	self.fwhm_text=Label(master,text='fwhm',bg='grey')
	self.fwhm_text.pack()
	self.fwhm_text.place(x=900,y=340,width=70,height=22)
	self.fwhm_get=Entry(master,bg='grey')
	self.fwhm_get.insert(0,'')
	self.fwhm_get.pack()
	self.fwhm_get.place(x=975,y=340,width=210,height=22)
	
	self.IMAGE_MAKER_text=Label(master,text='SPECTRA',width=45,bg='grey')
	self.IMAGE_MAKER_text.pack()
	self.IMAGE_MAKER_text.place(x=10,y=350)
	self.IMAGE_text=Label(master,text='images',width=10,bg='grey')
	self.IMAGE_text.pack()
	self.IMAGE_text.place(x=10,y=380)
	self.IMAGE_get=Entry(master,bg='grey',width=40)
	self.IMAGE_get.insert(0,'arcos.fits')
	self.IMAGE_get.pack()
	self.IMAGE_get.place(x=90,y=380)
	
	self.CURVE_text=Label(master,text='calibration',width=10,bg='grey')
	self.CURVE_text.pack()
	self.CURVE_text.place(x=10,y=410)
	self.CURVE_get=Entry(master,bg='grey',width=40)
	self.CURVE_get.insert(0,'wave.fits')
	self.CURVE_get.pack()
	self.CURVE_get.place(x=90,y=410)

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
	def spectra_image(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
		global intensity
		global mean
		global fwhm
		global background
		global MASTER_IMAGE
		global pixel_base
		
		image_list=self.IMAGE_get.get()
		
		
		name=self.CURVE_get.get()
		try:
			#lectura fichero
			hdul = fits.open(name)
			t = hdul['VALUES'].data
			hdul.close()
			wavelength_array=t.field(0)
			mean_array=t.field(1)
			fwhm_array=t.field(2)
			intensity_array=t.field(3)
			
			#ajuste curva
			if len(mean_array)-1<7:
				g_init=models.Polynomial1D(degree=len(mean_array)-1)
			else:
				g_init=models.Polynomial1D(degree=3)
			fit_g=fitting.LinearLSQFitter()
			
			pixel_wave=fit_g(g_init,mean_array,wavelength_array)
			wave_pixel=fit_g(g_init,wavelength_array,mean_array)
		except:
			g_init=models.Linear1D()
			fit_g=fitting.LinearLSQFitter()
			wave_pixel=fit_g(g_init,np.array([1,2,3]),np.array([1,2,3]))
			
		arc_images=read_list(image_list)
		for j in range(len(arc_images)):
			if j==0:
				arc_data=np.array(read_image(arc_images[j])) 
			else:
				arc_data=np.dstack((arc_data,np.array(read_image(arc_images[j])))) 

		#Cut image
		try:
			arc_x_1,arc_x_2,arc_y_1,arc_y_2=int(self.Ymin_value.get()),int(self.Ymax_value.get()),int(self.Xmin_value.get()),int(self.Xmax_value.get())
		except:
			pass
		
		#Selection of combining method
		combining_method=combining.get()
		combining_method_2=combining_2.get()
		turn=self.turn_get.get()
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
			print('only one image has been founded')
		
		if combining_method_2=='average':
			if turn=='yes':
				MASTER_IMAGE=np.mean(arc_data,axis=1)
				MASTER_IMAGE_std=np.std(arc_data,axis=1)
			else:
				MASTER_IMAGE=np.mean(arc_data,axis=0)
				MASTER_IMAGE_std=np.std(arc_data,axis=0)
		else:
			if turn=='yes':
				MASTER_IMAGE=np.median(arc_data,axis=1)
				MASTER_IMAGE_std=np.std(arc_data,axis=1)
			else:
				MASTER_IMAGE=np.median(arc_data,axis=0)
				MASTER_IMAGE_std=np.std(arc_data,axis=0)
				
		try:
			if turn=='yes':
				MASTER_IMAGE=MASTER_IMAGE[int(arc_x_1):int(arc_x_2)]#,int(arc_y_1):int(arc_y_2)
				pixel_base=np.linspace(arc_x_1,arc_x_2-1,arc_x_2-arc_x_1)
				min_pixel=arc_x_1
			else:
				MASTER_IMAGE=MASTER_IMAGE[int(arc_y_1):int(arc_y_2)]#,int(arc_y_1):int(arc_y_2)
				pixel_base=np.linspace(arc_y_1,arc_y_2-1,arc_y_2-arc_y_1)
				min_pixel=arc_y_1
		except:
			pixel_base=np.linspace(0,len(MASTER_IMAGE)-1,len(MASTER_IMAGE))
			min_pixel=0
		
		try:
			mean=float(self.mean_get.get())
		except:
			pass	
		try:
			intensity=float(self.intensity_get.get())
		except:
			pass
		try:
			fwhm=float(self.fwhm_get.get())
		except:
			pass
		try:
			background=float(self.background_get.get())
		except:
			pass
		
		
		fig, ax = plt.subplots()
		#axoff_fun(ax)
		
		try:
			pixel_base=pixel_wave(pixel_base)
			ax.set_xlabel('Wavelength')
		except:
			ax.set_xlabel('pixel')
		
		function=function_model.get()
		#fit a spectral line
		
		try:
			if type(mean)==float:
				if function=='gaussian':
					g_init=models.Gaussian1D(amplitude=intensity,mean=mean,stddev=fwhm/2.35)+models.Const1D(amplitude=background)
					fit_g=fitting.LevMarLSQFitter()
					g=fit_g(g_init,pixel_base[int(wave_pixel(mean-3*fwhm)-min_pixel):int(wave_pixel(mean+3*fwhm)-min_pixel)],MASTER_IMAGE[int(wave_pixel(mean-3*fwhm)-min_pixel):int(wave_pixel(mean+3*fwhm)-min_pixel)])
					intensity,fwhm,mean,background=g[0].amplitude[0],g[0].stddev[0]*2.35,g[0].mean[0],g[1].amplitude[0]
					#display information
					print('\n \n spectral line')
					print('------------')
					print('Type gaussian')
					print('Intensity = (', g[0].amplitude[0],')')
					print('Fwhm = (',g[0].stddev[0]*2.35,')')
					print('central pixel = (',g[0].mean[0],')')
					print('Background =(',g[1].amplitude[0],')')
				elif function=='voigt':
					g_init=models.Voigt1D(x_0=mean,amplitude_L=intensity,fwhm_L=fwhm/2,fwhm_G=fwhm/2)+models.Const1D(amplitude=background)
					fit_g=fitting.LevMarLSQFitter()
					g=fit_g(g_init,pixel_base[int(wave_pixel(mean-3*fwhm)-min_pixel):int(wave_pixel(mean+3*fwhm)-min_pixel)],MASTER_IMAGE[int(wave_pixel(mean-3*fwhm)-min_pixel):int(wave_pixel(mean+3*fwhm)-min_pixel)])
					intensity,fwhm,mean,background=g[0].amplitude_L[0],g[0].fwhm_L/2+(g[0].fwhm_L/4+g[0].fwhm_G)**0.5,g[0].x_0[0],g[1].amplitude[0]
					#display information
					print('\n \n spectral line')
					print('------------')
					print('Type voigt')
					print('Intensity = (', g[0](g[0].x_0),')')
					print('Fwhm = (',g[0].fwhm_L/2+(g[0].fwhm_L/4+g[0].fwhm_G)**0.5,')')
					print('central pixel = (',g[0].x_0[0],')')
					print('Background =(',g[1].amplitude[0],')')
				elif function=='lorentz':
					g_init=models.Lorentz1D(amplitude=intensity,x_0=mean,fwhm=fwhm)+models.Const1D(amplitude=background)
					fit_g=fitting.LevMarLSQFitter()
					g=fit_g(g_init,pixel_base[int(wave_pixel(mean-3*fwhm)-min_pixel):int(wave_pixel(mean+3*fwhm)-min_pixel)],MASTER_IMAGE[int(wave_pixel(mean-3*fwhm)-min_pixel):int(wave_pixel(mean+3*fwhm)-min_pixel)])
					intensity,fwhm,mean,background=g[0].amplitude[0],g[0].fwhm[0],g[0].x_0[0],g[1].amplitude[0]
					#display information
					print('\n \n spectral line')
					print('------------')
					print('Type lorentz')
					print('Intensity = (', g[0].amplitude[0],')')
					print('Fwhm = (',g[0].fwhm[0],')')
					print('central pixel = (',g[0].x_0[0],')')
					print('Background =(',g[1].amplitude[0],')')
				
		except:
			pass
	
		
		
		ax.yaxis.set_label_position('right')
		ax.xaxis.set_label_position('top')
		ax.set_ylabel('Intensity (counts)')
		try:
			ax.plot(pixel_base,MASTER_IMAGE,'g')
		except:
			ax.plot(pixel_base,MASTER_IMAGE,'g')
		try:
			ax.plot(pixel_base,g(pixel_base),'b')
		except:
			pass

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
	combining_2 = StringVar(master)
	combining_2.set("average") # initial value
	
	self.combining_text=Label(master,text='Combining images',width=20,bg='grey')
	self.combining_text.pack()
	self.combining_text.place(x=10,y=260,height=30)
	self.combining_get = OptionMenu(master, combining, 'average', 'median')
	self.combining_get.config(width=10,bg='grey',highlightthickness=0)
	self.combining_get.pack()
	self.combining_get.place(x=200,y=260,height=30)
	
	self.combining_2_text=Label(master,text='Combining lines',width=20,bg='grey')
	self.combining_2_text.pack()
	self.combining_2_text.place(x=10,y=300,height=30)
	self.combining_2_get = OptionMenu(master, combining, 'average', 'median')
	self.combining_2_get.config(width=10,bg='grey',highlightthickness=0)
	self.combining_2_get.pack()
	self.combining_2_get.place(x=200,y=300,height=30)
	
	def save_spectra(*event):
		global MASTER_IMAGE
		global pixel_base
		name=self.save_image_name.get()
		
		pixeles=np.linspace(0,len(MASTER_IMAGE)-1,len(MASTER_IMAGE))
		
		try:
			c1 = fits.Column(name='pixel',array=pixeles, format='E')
			c2 = fits.Column(name='wavelength',array=pixel_base, format='E')
			c3 = fits.Column(name='intensity',array=MASTER_IMAGE, format='E')
			t = fits.BinTableHDU.from_columns([c1,c2,c3],name='VALUES')
			t.writeto(name+'.fits',overwrite=True)
			
		except:
			print('no available spectra to save')
		
		
			
	self.save_image_text=Button(master,text='Save spectra as',width=20,bg='grey',command=save_spectra)
	self.save_image_text.pack()
	self.save_image_text.place(x=400,y=620)
	self.save_image_name=Entry(master,bg='grey')
	self.save_image_name.insert(0,'insert name')
	self.save_image_name.pack()
	self.save_image_name.place(x=560,y=620,width=200,height=30)
	
	self.combining_button=Button(master,text='Make spectra',width=20,command=spectra_image,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)
	
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

