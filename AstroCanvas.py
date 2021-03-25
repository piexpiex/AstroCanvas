import numpy as np
from modes.BIAS import *
from modes.DARKS import *
from modes.FLATS import *
from modes.REDUCTION import *
from modes.SPECTRAL_ARCS import *
from modes.SPECTRA import *
from modes.RGB_MAKER import *
from modes.GREY_MAKER import *
from modes.CONTOUR_MAP import *
from modes.LIGHTCURVE_MAKER import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import BoundaryNorm
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from tkinter import *
import sys
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from astropy.modeling import models, fitting

class App:
	def __init__(self, master,imagen,icono):
		master.geometry('1200x700')
		master.configure(bg='black') #333300 verde oscuro
		master.wm_title("AstroCanvas")
		master.iconphoto(True,icono)
		
		#AstroCanvas logo
		
		self.basic_Logo=Label(master, image=imagen, bd=0)
		self.basic_Logo.config(width=1200,height=59,bg='black')
		self.basic_Logo.pack()
		self.basic_Logo.place(x=0,y=0)
		
		#exit buttom
		
		self.basic_exit_get=Button(master,text='exit',width=10,command=master.quit,bg='grey')
		self.basic_exit_get.pack()
		self.basic_exit_get.place(x=1100,y=0)
		
		#initial canvas
		
		fig, ax = plt.subplots()
		#fig.set_size_inches(4.5, 4.5)
		#axoff_fun = np.vectorize(lambda ax:ax.axis('off'))
		# ... stuff here ...
		#axoff_fun(ax)
		#fig.savefig('test2png.png', dpi=100)
		#self.Canvas_text=Label(master,text='CURRENTLY IMAGE',width=64,bg='grey')
		#self.Canvas_text.pack()
		#self.Canvas_text.place(x=400,y=100)
		#self.canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
		#self.canvas.draw()
		#self.canvas.get_tk_widget().place(x=400,y=150)
		
		#Select theme
		def _theme(*event):       #colores de los botones y de las letras
			if theme.get()=='white':
				logo_color='white'
				color='white'
			elif theme.get()=='black':
				logo_color='black'
				color='black'
			elif theme.get()=='blue':
				logo_color='blue'
				color='blue'
			self.basic_Logo.config(width=1200,height=60,bg=logo_color)
			master.configure(bg=color)
		theme = StringVar(master)
		theme.set("black") # initial value
		self.basic_theme_text=Label(master,text='Color scheme',width=10,bg='grey') #or theme
		self.basic_theme_text.pack()
		self.basic_theme_text.place(x=10,y=100,height=25)
		self.basic_theme_get = OptionMenu(master, theme, 'white', 'black','blue')
		self.basic_theme_get.config(width=15,bg='grey',highlightthickness=0)
		self.basic_theme_get.pack()
		self.basic_theme_get.place(x=100,y=100,height=25)
		theme.trace('w',_theme)

		#Select mode 

		mode = StringVar(master)
		mode.set("grey images") # initial value
		self.basic_mode_text=Label(master,text='Mode',width=10,bg='grey')
		self.basic_mode_text.pack()
		self.basic_mode_text.place(x=10,y=150,height=25)
		self.basic_mode_get = OptionMenu(master, mode,'bias','darks','flats','image reduction','spectral arcs','spectra', 'rgb images', 'grey images','contour map','lightcurve')
		self.basic_mode_get.config(width=15,bg='grey',highlightthickness=0)
		self.basic_mode_get.pack()
		self.basic_mode_get.place(x=100,y=150,height=25)

		def destroy_app(self):
			for var in vars(self):
				if var[0:5]=='basic':
					continue
				elif var[0:6]=='canvas':
					try:
						_=self.canvas.toolbar.destroy()
					except:
						pass
					_=self.canvas.get_tk_widget().destroy()
				else:
					exec('self.'+var+'.destroy()')
				
		def _mode(*event):
			if mode.get()=='bias':
				_=destroy_app(self)
				_=BIAS_IMAGES(self,master)
			elif mode.get()=='darks':
				_=destroy_app(self)
				_=DARK_IMAGES(self,master)
			elif mode.get()=='flats':
				_=destroy_app(self)
				_=FLAT_IMAGES(self,master)
			elif mode.get()=='image reduction':
				_=destroy_app(self)
				_=CALIBRATION_IMAGES(self,master)
			elif mode.get()=='spectral arcs':
				_=destroy_app(self)
				_=SPECTRAL_ARCS(self,master)
			elif mode.get()=='spectra':
				_=destroy_app(self)
				_=SPECTRA(self,master)
			elif mode.get()=='rgb images':
				_=destroy_app(self)
				_=RGB_IMAGES(self,master)
			elif mode.get()=='grey images':
				_=destroy_app(self)
				_=GREY_IMAGES(self,master)
			elif mode.get()=='contour map':
				_=destroy_app(self)
				_=CONTOUR_MAP(self,master)
			elif mode.get()=='lightcurve':
				_=destroy_app(self)
				_=LIGHTCURVE(self,master)
		
		mode.trace('w',_mode)

		
		print('Starting AstroCanvas')
		#self.basic_destroy = Button(master,text="destroy",width=10,command=self.destroy_app,bg='grey')
		#self.basic_destroy.pack()
		#self.basic_destroy.place(x=1100,y=30)
		#print(vars(self))
		
	def destroy_app(self):
		for var in vars(self):
			if var[0:5]=='basic':
				continue
			elif var[0:6]=='canvas':
				try:
					_=self.canvas.toolbar.destroy()
				except:
					pass
				_=self.canvas.get_tk_widget().destroy()
			else:
				print('self.'+var+'.destroy()')
				exec('self.'+var+'.destroy()')

root = Tk()
imagen = PhotoImage(file="configuration/Logo.gif")
icono = PhotoImage(file="configuration/Icon.gif")
app = App(root,imagen,icono)
root.mainloop()
print('exit from AstroCanvas')
