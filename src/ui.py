# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *
from protocols import *
from funcs import *
from galaxy_evaluator import *
from lists import *

UI_SCALE=3

PROTOCOL=evaluate_galaxy #statefuldraw

class TkUI:
  def __init__(self):
    self.root = Tk()

    self.canvas = Canvas(self.root, width=1000, height=1000, bg='black')
    self.center = (500, 500)
    self.canvas.bind("<Button-1>", self.handle_click)
    # self.canvas.bind("<Double-Button-1>", self.handle_double_click)
    self.canvas.pack()

    # Initial states:
    #
    #  boot up sequence
    # self.current_state = list_to_cons([2, [1, -1], 0, []])
    #
    #  show galaxy, click around to see races:
    self.current_state = list_to_cons([1, [11], 0, []])

    self.interact(0, 0)

  def handle_double_click(self, event):
      print(f"click all pixels")
      ui_elements = recursive_list_convert(self.current_img_data)[:-1]
      for pixels in ui_elements:
          for x, y in pixels:
              current_ui_elements = recursive_list_convert(self.current_img_data)[:-1]
              if ui_elements != current_ui_elements:
                  print('image changed:', ui_elements, current_ui_elements)
                  break
              self.interact(x, y)
              self.interact(x+1, y+1)
              self.interact(x+1, y)
              self.interact(x+1, y-1)
              self.interact(x, y-1)
              self.interact(x-1, y-1)
              self.interact(x-1, y)
              self.interact(x-1, y+1)
              self.interact(x, y+1)

  def handle_click(self, event):
      x = int(round((event.x - self.center[0]) / UI_SCALE - 0.5))
      y = int(round((event.y - self.center[1]) / UI_SCALE - 0.5))
      print(f"clicked at {x} {y}")
      self.interact(x, y)

  def interact(self, x, y):
      click = Ap(Ap(cons, Atom(str(x))), Atom(str(y)))
      (new_state, img_data) = interact(PROTOCOL, self.current_state, click)
      # print(f"new_state = {new_state} img_data={img_data}")
      self.current_img_data = img_data
      self.current_state = new_state

      # clean canvas before draw
      self.canvas.delete(ALL)
      # quick, draw!
      multipledraw_helper(img_data, draw_dot_impl=self.add_pixel)

  def add_pixel(self, x, y, index):
    # colors = ["white", "blue", "red", "green"]
    fade = 0.5**index
    intensity = round(255.0*fade)
    intensity_hex = hex(intensity)[2:].zfill(2)
    fill_color = f'#{intensity_hex*3}'
    self.canvas.create_rectangle(
      x * UI_SCALE + self.center[0],
      y * UI_SCALE + self.center[1],
      (x + 1) * UI_SCALE + self.center[0],
      (y + 1) * UI_SCALE + self.center[1],
      width=0.25,
      activefill='#ff7f00',
      fill=fill_color)

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
