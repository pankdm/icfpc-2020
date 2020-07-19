# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *
from protocols import *
from funcs import *
from galaxy_evaluator import *

UI_SCALE=4

PROTOCOL=evaluate_galaxy #statefuldraw

class TkUI:
  def __init__(self):
    self.root = Tk()

    self.canvas = Canvas(self.root, width=700, height=700)
    self.center = (350, 350)
    self.canvas.bind("<Button-1>", self.handle_click)
    self.canvas.pack()

    self.current_state = nil
    self.interact(0, 0)

  def handle_click(self, event):
      (x, y) = (int((event.x - self.center[0]) / UI_SCALE), int((event.y - self.center[1]) / UI_SCALE))
      print(f"clicked at {x} {y}")

      self.canvas.delete(ALL)
      
      self.interact(x, y)

  def interact(self, x, y):
      click = Ap(Ap(cons, Atom(str(x))), Atom(str(y)))
      (new_state, img_data) = interact(PROTOCOL, self.current_state, click)
      print(f"new_state = {new_state} img_data={img_data}")
      self.current_state = new_state

      multipledraw_helper(img_data, draw_dot_impl=self.add_pixel)

  def add_pixel(self, x, y):
    self.canvas.create_rectangle(
      x * UI_SCALE + self.center[0],
      y * UI_SCALE + self.center[1],
      (x + 1) * UI_SCALE + self.center[1],
      (y + 1) * UI_SCALE + self.center[1],
      fill="black")

  def mainloop(self):
    self.root.mainloop()


def main():
  # as_expr = list_to_cons([1,2,3,[4]])
  # print(f"as_expr {as_expr}")
  # as_list = recursive_list_convert(as_expr)
  # print(f"as_list {as_list}")
  # exit()

  sys.setrecursionlimit(10000)
  load_galaxy_from_source(sys.argv[1])

  ui = TkUI()
  ui.mainloop()

if __name__ == "__main__":
  main()
