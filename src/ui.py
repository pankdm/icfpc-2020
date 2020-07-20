# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *
from funcs import *
from galaxy_evaluator import *
from lists import *
from interact import *

UI_SCALE=3

PROTOCOL=evaluate_galaxy #statefuldraw

class TkUI:
  def __init__(self):
    self.root = Tk()

    width = 330 * UI_SCALE
    height = 300 * UI_SCALE
    self.canvas = Canvas(self.root, width=width, height=height, bg='black')
    self.center = (width / 2, height / 2)
    self.canvas.bind("<Button-1>", self.handle_click)
    self.canvas.bind("<Shift-A>", self.handle_click_all_pixels)
    self.canvas.bind("<BackSpace>", self.handle_rewind)
    self.canvas.bind("<Key>", self.handle_key)
    self.canvas.pack()
    self.current_img_data = None


    self.selected_layer = None

    # Initial states:
    #
    #  boot up sequence
    # self.current_state = nil
    #
    #  show galaxy, click around to see races:
    self.current_state = py_to_tree([1, [11], 0, None])

    # before tutorials
    # self.current_state = py_to_tree([6, [1, 8, 5786732064739500194, 1, 0, 0, [], [], 4, [0, [], [[[1, 0, (16, 0), (1, 0), [0, 0, 0, 1], 0, 64, 1], []]]], [8, 1, [448, 1, 64], [], []], [], []], 8, []])
    
    # self.current_state = py_to_tree(
    #   # [5, [1, 0, [], [], [], [], [], 16701], 8, []]  # before tutorials
    #   [1, [11], 0, None]
    #   )
    #
    #  some picture with increasing boxes
    # self.current_state = py_to_tree([2, [4, 5], 0, []])
    #

    # before tutorial
    self.current_state = py_to_tree([5, [2, 0, [], [], [], [], [], 14571], 8, []])

    #  glyphs guessing game
    # self.current_state = py_to_tree([4, [1, [122, 203, 410, 164, 444, 484, 202, 77, 251, 56, 456, 435, 28, 329, 257, 265, 501, 18, 190, 423, 384, 434, 266, 69, 34, 437, 203, 152, 160, 425, 245, 428, 99, 107, 192, 372, 346, 344, 169, 478, 393, 502, 201, 497, 313, 32, 281, 510, 436, 22, 237, 80, 325, 405, 184, 358, 57, 276, 359, 189, 284, 277, 198, 244], -1, 0, []], 0, []])
    #
    #  riddle with beams
    # self.current_state = py_to_tree([2, [3, 1], 0, []])
    #
    #  donut game (tic-tac-toe?)
    # self.current_state = py_to_tree([3, [0, [0, 0, 0, 0, 0, 0, 0, 0, 0], [], 0], 0, []])
    #
    #  end game
    # self.current_state = py_to_tree([5, [2, 0, [], [], [], [], [], 39392], 125, []])

    # start from galaxy screen:
    # self.current_state = py_to_tree([5, [2, 0, [], [], [], [], [], 39656], 125, []])

    # end game?
    # self.current_state = py_to_tree([10, [], 8, []])
    # tutorial 1 state:
    # self.current_state = py_to_tree([6, [2, 5, 0, 1, 1, 0, [], [], 4, [], [], [], []], 8, []])
    # self.current_state = py_to_tree([6, [3, 5, 0, 1, 11, 0, [], [], 4, [], [], [], []], 8, []])
    # self.current_state = py_to_tree([6, [3, 5, 0, 1, 11, 0, [], [], 4, [], [], [], []], 8, []])
    # self.current_state = py_to_tree([6, [4, 5, 0, 1, 21, 0, [], [], 4, [], [], [], []], 8, []])

    self.state_click_history = []
    self.img_history = [None]

    data = None

    # tutorial 1
    self.current_state = py_to_tree([6, [2, 5, 0, 1, 1, 0, [], [], 4, [], [], [], []], 8, []])    
    data = [1, 2]

    # tutorial 2
    self.current_staet = py_to_tree([6, [3, 5, 0, 1, 9, 0, [], [], 4, [], [], [], []], 8, []])
    data = [1, 3]

    # tutorial 6
    self.current_staet = py_to_tree([6, [6, 5, 0, 1, 9, 0, [], [], 4, [], [], [], []], 8, []])
    data = [1, 6]



    if data:
      self.interact_with_data(data)
    else:
      self.interact(0, 0)

  def handle_key(self, event):
      ch = event.char
      print(f"\nKey '{ch}' was pressed: {self.selected_layer}")
      if ch in ['1', '2', '3', '4', '5', '6', '7']:
        code = int(ch)
        layer = code - 1
        if self.selected_layer == layer:
          self.selected_layer = None
        else:
          self.selected_layer = layer
        self.draw()

  def handle_rewind(self, event):
      print(f'\n\nAttempting time travel...')
      self.rewind_state()

  def handle_click_all_pixels(self, event):
      print(f"click all pixels")
      ui_elements = tree_to_py(self.current_img_data)[:-1]
      for pixels in ui_elements:
          for x, y in pixels:
              current_ui_elements = tree_to_py(self.current_img_data)[:-1]
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
      self.canvas.focus_set()

  def update_state(self, current_state, img_data, click, next_state, next_img_data):
      if tree_to_py(current_state) != tree_to_py(next_state):
          self.state_click_history.append((current_state, click))
          self.img_history.append(img_data)
          self.current_state = next_state
          self.current_img_data = next_img_data

  def rewind_state(self):
      if (len(self.state_click_history) > 1):
          print('Rewind state, time travel, Morty!')
          prev_state, prev_click = self.state_click_history.pop()
          prev_img_data = self.img_history.pop()
          self.current_state = prev_state
          self.current_img_data = prev_img_data
          self.draw()
      else:
          print('Already at the earliest state.')


  def draw(self):
      # clean canvas before draw
      self.canvas.delete(ALL)
      # quick, draw!
      multipledraw_helper(
        self.current_img_data, 
        draw_dot_impl=self.add_pixel,
        selected_layer=self.selected_layer)

  def interact(self, x, y):
      click = Ap(Ap(cons, Val(x)), Val(y))
      (new_state, img_data) = interact(PROTOCOL, self.current_state, click)
      # print(f"new_state = {new_state} img_data={img_data}")
      self.update_state(self.current_state, self.current_img_data, (x, y), new_state, img_data)
      self.draw()

  def interact_with_data(self, data):
      sent = my_send_to_alien_proxy(data)
      (new_state, img_data) = interact(PROTOCOL, self.current_state, sent)
      # print(f"new_state = {new_state} img_data={img_data}")
      self.update_state(self.current_state, self.current_img_data, (0, 0), new_state, img_data)
      self.draw()


  def add_pixel(self, x, y, index):
    colors = ["white", "cyan", "red", "green", "orange", "blue", "yellow", "magenta"]
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
      fill=colors[index])

  def mainloop(self):
    self.root.mainloop()


def main():
  # as_expr = py_to_tree([1,2,3,[4]])
  # print(f"as_expr {as_expr}")
  # as_list = tree_to_py(as_expr)
  # print(f"as_list {as_list}")
  # exit()

  sys.setrecursionlimit(10000)
  load_galaxy_from_source(sys.argv[1])

  ui = TkUI()
  ui.mainloop()

if __name__ == "__main__":
  main()
