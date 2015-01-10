from Tkinter import *
from ttk import Style
import bitmesh

class ClientWindow(Frame):

	# width of the window
	w = int(500)
	# height of the window
	h = int(500)

	def __init__(self, parent):
		# Frame for the whole window
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.centerWindow()
		self.initUI()

	def initUI(self):
		self.parent.title("Bitmesh Client")
		self.style = Style()
		self.style.theme_use("default")
		self.pack(fill=BOTH, expand=1)

		# set up the grid on the frame. Feels a lot like 
		# "GridBagLayout" from java.swing
		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=1)
		
		# establish text area with border of 1 that is "Sunken"
		self.log_text_area = Text(self, bd=1, relief=SUNKEN)
		self.log_text_area.insert(END,"BEGIN LOG\n---------")
		# Texts have to be in state normal to be modified. I am doing this
		# so the user doesn't edit the log
		self.log_text_area.config(state=DISABLED)
		self.log_text_area.grid(row=1, column=0, columnspan=2, rowspan=4, sticky=E+W+S+N)
		
		self.connect_button = Button(self, text="Connect")
		# TODO: attempting to strech the button across the grid
		self.connect_button.grid(row=1, column=2, sticky=E+W+N)
		self.connect_button.bind("<Button-1>", self.connect_callback)

		self.request_text_area = Text(self, height=1, bd=1, relief=SUNKEN)
		self.request_text_area.grid(row=0 ,column=1, sticky=E+W)

		self.request_website_button = Button(self, text="Request Site")
		self.request_website_button.grid(row=0, column=0, columnspan=1, sticky=W+N)
		self.request_website_button.bind("<Button-1>", self.request_callback)

	# on connect_button left clicked
	def connect_callback(self,event):
		self.log_text_area.config(state=NORMAL)
		self.log_text_area.insert(END,"\nConnecting to: "+"IP/"+":"+"PORT")
		self.log_text_area.config(state=DISABLED)
		# bitmesh.buy_data

	def request_callback(self,event):
		self.log_text_area.config(state=NORMAL)
		self.log_text_area.insert(END,"\nFetching website: " + self.request_text_area.get(1.0,END))
		self.log_text_area.config(state=DISABLED)

	# centers the window in the client's screen
	def centerWindow(self):  
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - self.w)/2
		y = (sh - self.h)/2
		self.parent.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

# start up the client GUI
def start_client():
	root = Tk()
	app = ClientWindow(root)
	root.mainloop()