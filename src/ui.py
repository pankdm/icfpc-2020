# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *

UI_SCALE=2

class TkUI:
	def __init__(self):
		self.root = Tk()

		self.canvas = Canvas(self.root, width=500, height=500)
		self.canvas.bind("<Button-1>", self.handle_click)
		self.canvas.pack()		

	def handle_click(self, event):
	    print(f"clicked at {event.x} {event.y}")

	    self.canvas.delete(ALL)
	    self.add_pixel(event.x / UI_SCALE, event.y / UI_SCALE)

	def add_pixel(self, x, y):
		self.canvas.create_rectangle(x * UI_SCALE, y * UI_SCALE, (x + 1) * UI_SCALE, (y + 1) * UI_SCALE, fill="black")		

	def mainloop(self):
		self.root.mainloop()

ui = TkUI()
ui.mainloop()
