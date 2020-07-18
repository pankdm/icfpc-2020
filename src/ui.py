# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *
from protocols import *
from funcs import *

UI_SCALE=2
PROTOCOL=statefuldraw

class TkUI:
  def __init__(self):
    self.root = Tk()

    self.canvas = Canvas(self.root, width=500, height=500)
    self.canvas.bind("<Button-1>", self.handle_click)
    self.canvas.pack()

    self.current_state = NIL
    self.interact(0, 0)

  def handle_click(self, event):
      print(f"clicked at {event.x} {event.y}")
      (x, y) = (event.x / UI_SCALE, event.y / UI_SCALE)

      self.canvas.delete(ALL)
      
      self.interact(x, y)

  def interact(self, x, y):
      (new_state, img_data) = interact(PROTOCOL, self.current_state, [x, y])
      print(f"new_state = {new_state} img_data={img_data}")
      self.current_state = new_state

      multipledraw_helper(img_data, draw_dot_impl=self.add_pixel)

  def add_pixel(self, x, y):
    self.canvas.create_rectangle(x * UI_SCALE, y * UI_SCALE, (x + 1) * UI_SCALE, (y + 1) * UI_SCALE, fill="black")    

  def mainloop(self):
    self.root.mainloop()

ui = TkUI()
ui.mainloop()
