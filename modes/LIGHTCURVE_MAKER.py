import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from astropy.io import fits
from astropy.timeseries import BoxLeastSquares,TimeSeries,aggregate_downsample
from astropy.time import Time
from astropy import units as u
from astropy.table import Table
from tkinter import *
import sys
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import warnings
warnings.filterwarnings('ignore')

def LIGHTCURVE(self,master):
	#-------creation of lightcurve from a fits table----------
	
	self.TPERIOD_text=Label(master,text='period',bg='grey')
	self.TPERIOD_text.pack()
	self.TPERIOD_text.place(x=900,y=200,width=70,height=22)
	self.TPERIOD_get=Entry(master,bg='grey')
	self.TPERIOD_get.insert(0,'')
	self.TPERIOD_get.pack()
	self.TPERIOD_get.place(x=975,y=200,width=210,height=22)
	
	self.TSTART_text=Label(master,text='time start',bg='grey')
	self.TSTART_text.pack()
	self.TSTART_text.place(x=900,y=228,width=70,height=22)
	self.TSTART_get=Entry(master,bg='grey')
	self.TSTART_get.insert(0,'')
	self.TSTART_get.pack()
	self.TSTART_get.place(x=975,y=228,width=210,height=22)
	
	self.NBINS_text=Label(master,text='bins number',bg='grey')
	self.NBINS_text.pack()
	self.NBINS_text.place(x=900,y=256,width=70,height=22)
	self.NBINS_get=Entry(master,bg='grey')
	self.NBINS_get.insert(0,'')
	self.NBINS_get.pack()
	self.NBINS_get.place(x=975,y=256,width=210,height=22)
	
	self.MIN_PERIOD_text=Label(master,text='min period',bg='grey')
	self.MIN_PERIOD_text.pack()
	self.MIN_PERIOD_text.place(x=900,y=284,width=70,height=22)
	self.MIN_PERIOD_get=Entry(master,bg='grey')
	self.MIN_PERIOD_get.insert(0,'')
	self.MIN_PERIOD_get.pack()
	self.MIN_PERIOD_get.place(x=975,y=284,width=65,height=22)
	
	self.MAX_PERIOD_text=Label(master,text='max period',bg='grey')
	self.MAX_PERIOD_text.pack()
	self.MAX_PERIOD_text.place(x=1045,y=284,width=70,height=22)
	self.MAX_PERIOD_get=Entry(master,bg='grey')
	self.MAX_PERIOD_get.insert(0,'')
	self.MAX_PERIOD_get.pack()
	self.MAX_PERIOD_get.place(x=1120,y=284,width=65,height=22)
	
	self.PERIOD_BINS_text=Label(master,text='period bins',bg='grey')
	self.PERIOD_BINS_text.pack()
	self.PERIOD_BINS_text.place(x=900,y=312,width=70,height=22)
	self.PERIOD_BINS_get=Entry(master,bg='grey')
	self.PERIOD_BINS_get.insert(0,'')
	self.PERIOD_BINS_get.pack()
	self.PERIOD_BINS_get.place(x=975,y=312,width=210,height=22)

	self.LIGHTCURVE_MAKER_text=Label(master,text='LIGHTCURVE MAKER',width=45,bg='grey')
	self.LIGHTCURVE_MAKER_text.pack()
	self.LIGHTCURVE_MAKER_text.place(x=10,y=350)
	self.LIGHTCURVE_text=Label(master,text='bias images',width=10,bg='grey')
	self.LIGHTCURVE_text.pack()
	self.LIGHTCURVE_text.place(x=10,y=380)
	self.LIGHTCURVE_get=Entry(master,bg='grey',width=40)
	self.LIGHTCURVE_get.insert(0,'lightcurve.fits')
	self.LIGHTCURVE_get.pack()
	self.LIGHTCURVE_get.place(x=90,y=380)
	
	self.EXTENSION_text=Label(master,text='extension',width=10,bg='grey')
	self.EXTENSION_text.pack()
	self.EXTENSION_text.place(x=10,y=410)
	self.EXTENSION_get=Entry(master,bg='grey',width=40)
	self.EXTENSION_get.insert(0,'VALUES')
	self.EXTENSION_get.pack()
	self.EXTENSION_get.place(x=90,y=410)
	
	self.TIME_COLUMN_text=Label(master,text='times',width=10,bg='grey')
	self.TIME_COLUMN_text.pack()
	self.TIME_COLUMN_text.place(x=10,y=440)
	self.TIME_COLUMN_get=Entry(master,bg='grey',width=40)
	self.TIME_COLUMN_get.insert(0,'time')
	self.TIME_COLUMN_get.pack()
	self.TIME_COLUMN_get.place(x=90,y=440)
	
	self.INTENSITY_COLUMN_text=Label(master,text='intensity',width=10,bg='grey')
	self.INTENSITY_COLUMN_text.pack()
	self.INTENSITY_COLUMN_text.place(x=10,y=470)
	self.INTENSITY_COLUMN_get=Entry(master,bg='grey',width=40)
	self.INTENSITY_COLUMN_get.insert(0,'intensity')
	self.INTENSITY_COLUMN_get.pack()
	self.INTENSITY_COLUMN_get.place(x=90,y=470)

	def read_table(image,extension,times,intensity):  #(LIGHTCURVE_images[j],LIGHTCURVE_extension,LIGHTCURVE_times,LIGHTCURVE_intensity)
		if intensity==0:
			image_name=str(image)
			if image_name[len(image_name)-5:]=='.fits':
				image_data=fits.open(image_name)[extension].data
				
				hdul = fits.open(image_name)
				image_data = hdul[extension].data
				hdul.close()
				image_times=image_data.field(times)
			else:
				print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS')
				
			return(image_times) 
		else:
			image_name=str(image)
			if image_name[len(image_name)-5:]=='.fits':
				image_data=fits.open(image_name)[extension].data
				
				hdul = fits.open(image_name)
				image_data = hdul[extension].data
				hdul.close()
				image_times=image_data.field(times)
				image_intensities=image_data.field(intensity)
			else:
				print('the format of the image is not avalaible \n please try with one of these formats: \n     FITS')
				
			return(image_times,image_intensities) 
		
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
	def lightcurve(*event):
		#destroy previous canvas to save memory
		try:
			_=self.canvas.toolbar.destroy()
		except:
			pass
		try:
			_=self.canvas.get_tk_widget().destroy()
		except:
			pass
		
		global t_fit
		global y_fit
		
		LIGHTCURVE_list=self.LIGHTCURVE_get.get()
		LIGHTCURVE_images=read_list(LIGHTCURVE_list)
		LIGHTCURVE_extension=self.EXTENSION_get.get()
		LIGHTCURVE_times=self.TIME_COLUMN_get.get()
		if self.INTENSITY_COLUMN_get.get()=='':
			LIGHTCURVE_intensity=0
		else:
			LIGHTCURVE_intensity=self.INTENSITY_COLUMN_get.get()
			
		if LIGHTCURVE_intensity==0:
			for j in range(len(LIGHTCURVE_images)):
				if j==0:
					time_data=np.array(read_table(LIGHTCURVE_images[j],LIGHTCURVE_extension,LIGHTCURVE_times,0))
					intensity_data=np.ones(len(time_data))
				else:
					time_data,intensity_data=np.dstack((LIGHTCURVE_data,np.array(read_table(LIGHTCURVE_images[j],LIGHTCURVE_extension,LIGHTCURVE_times,LIGHTCURVE_intensity))))
		else:
			for j in range(len(LIGHTCURVE_images)):
				if j==0:
					time_data,intensity_data=np.array(read_table(LIGHTCURVE_images[j],LIGHTCURVE_extension,LIGHTCURVE_times,LIGHTCURVE_intensity))
				else:
					print('Only the first fits was analyzed')
		
		
		#aqui van las cosas
		try:
			T_PERIOD=float(self.TPERIOD_get.get())
			period=T_PERIOD
		except:
			try:
				min_period=float(self.MIN_PERIOD_get.get())
				max_period=float(self.MAX_PERIOD_get.get())
				bin_period=int(self.PERIOD_BINS_get.get())
				results=BoxLeastSquares(time_data,intensity_data).power(np.linspace(min_period,max_period,bin_period),0.04) #.autopower(4) #LombScargle(time_data,intensity_data).autopower()
				period=results.period[np.argmax(results.power)]
				transit_time=results.transit_time[np.argmax(results.power)]
			
				best_frequency= 1.0/period#frequency[np.argmax(power)]
				self.TPERIOD_get.delete(0,'end')
				self.TPERIOD_get.insert(0,str(1.0/best_frequency))
			except:
				period=1.11
		try:
			T_START=float(self.TSTART_get.get())
			if T_START >0:
				while T_START>period:
					T_START=T_START-period
			elif T_START <0:
				while T_START<0:
					T_START=T_START+period
			#time_data=time_data-T_START
		except:
			T_START=0
		try:
			nbins=int(self.NBINS_get.get())
		except:
			nbins=50
		START_BIN=int(T_START*nbins/period)
		period=period*u.day
		cvcc=Time(val=time_data,format='mjd')
		tabla_time = Table({'data':np.array(intensity_data,dtype=float)})
		ts=TimeSeries(data=tabla_time,time=cvcc)
		ts_fold=ts.fold(period=period)
		TTG=Time(T_START,format='mjd')
		ts_binned=aggregate_downsample(time_series=ts_fold,time_bin_size=period/nbins) 
		
		y_fit=np.append(ts_binned['data'][START_BIN:len(ts_binned['data'])],ts_binned['data'][0:START_BIN])
		y_fit=np.append(y_fit,y_fit)
		fig, ax = plt.subplots()
		#axoff_fun(ax)
		ax.yaxis.set_label_position('right')
		ax.xaxis.set_label_position('top')
		ax.set_ylabel('Intensity (counts)')
		ax.set_xlabel('Phase')
		t_fit=np.linspace(0,2,2*len(ts_binned['data']))
		ax.step(t_fit,y_fit,where='mid',color='k') #ts_binned.time_bin_start.jd
		#ax.plot(ts_binned.time_bin_start.jd,ts_binned['data'],'k-',drawstyle='steps-post')
		#ax.step(t_fit,y_fit,where='mid',color='k')
		
		
		#plt.errorbar(Pulse_profiles[j].ph,Pulse_profiles[j].profilenorm,yerr=Pulse_profiles[j].profile_err,fmt=color[j]+'o',markersize=0.5)

	
		#ax.plot(t_fit,y_fit,'k')
		

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
		
		#display information
		print('\n \n Lightcurve')
		print('----------')
		print('period= (', period/u.day ,')')
	

	fig, ax = plt.subplots()
	fig.set_size_inches(4.5, 4.5)
	axoff_fun = np.vectorize(lambda ax:ax.axis('off'))
	# ... stuff here ...
	axoff_fun(ax)
	#fig.savefig('test2png.png', dpi=100)
	self.Canvas_text=Label(master,text='CURRENTLY TABLE',width=64,bg='grey')
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

	def save_lightcurve(*event):
		global t_fit
		global y_fit
		name=self.image_name.get()
		
		
		try:
			c1 = fits.Column(name='phase',array=t_fit, format='E')
			c2 = fits.Column(name='intensity',array=y_fit, format='E')
			#c3 = fits.Column(name='intensity',array=MASTER_IMAGE, format='E')
			t = fits.BinTableHDU.from_columns([c1,c2],name='VALUES')
			t.writeto(name+'.fits',overwrite=True)
			
		except:
			print('no available lightcurve to save')
	
	self.save_image_text=Button(master,text='Save lightcurve as',width=20,bg='grey',command=save_lightcurve)
	self.save_image_text.pack()
	self.save_image_text.place(x=400,y=620)
	self.image_name=Entry(master,bg='grey')
	self.image_name.insert(0,'insert name')
	self.image_name.pack()
	self.image_name.place(x=560,y=620,width=200,height=30)
	
	self.combining_button=Button(master,text='Make lightcurve',width=20,command=lightcurve,bg='grey')
	self.combining_button.pack()
	self.combining_button.place(x=10,y=590)
	
	
	


