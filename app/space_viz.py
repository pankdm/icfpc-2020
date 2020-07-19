# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *
from models import *

UI_SCALE=3


# in pixels
SPACE_SHIP_SIZE = 2

class SpaceUI:
  def __init__(self, responses):
    self.root = Tk()

    width = 300 * UI_SCALE
    height = 300 * UI_SCALE
    self.canvas = Canvas(self.root, width=width, height=height, bg='black')
    self.center = (width / 2, height / 2)

    self.canvas.bind("<Button-1>", self.handle_click)
    self.canvas.bind("<Key>", self.handle_key)
    self.canvas.pack()


    self.responses = responses
    self.index = 0

    self.draw()
    self.canvas.focus_set()

  def append_response(self, response):
    need_update = False
    if self.index + 1 >= len(self.responses):
      need_update = True
    self.responses.append(response)
    if need_update:
      self.index = len(self.responses) - 1
      self.draw()


  def handle_click(self, event):
      self.draw()
      self.canvas.focus_set()


  def handle_key(self, event):
    ch = event.char
    print(f"\nKey '{ch}' was pressed")
    if ch == 's':
      if self.index > 0:
        self.index -= 1
    elif ch == 'd':
      if self.index + 1 < len(self.responses):
        self.index += 1
    self.draw()


  def draw_planet(self):
    self.draw_rectangular((-16, -16), (16, 16), fill="white")

  def map_x_coord(self, x):
    return x * UI_SCALE + self.center[0]

  def map_y_coord(self, y):
    return y * UI_SCALE + self.center[1]

  def draw_gravity_field(self):
    left = -48
    right = 48
    step = 32
    for cc in range(left, right + step, step):
      self.draw_line(cc, left, cc, right)
      self.draw_line(left, cc, right, cc)
    
    coords = [(-48, -16), (48, 16)]
    for a, b in coords:
      self.draw_line(a, -a, b, -b)
      self.draw_line(a, a, b, b)
      

  def draw_line(self, x0, y0, x1, y1):
      green = "#3CB043"
      self.canvas.create_line(
        self.map_x_coord(x0),
        self.map_y_coord(y0),
        self.map_x_coord(x1),
        self.map_y_coord(y1), 
        fill=green)


  def draw_rectangular(self, p0, p1, **varargs):
    index = 0
    fade = 0.5**index
    intensity = round(255.0*fade)
    intensity_hex = hex(intensity)[2:].zfill(2)
    fill_color = f'#{intensity_hex*3}'
    cx, cy = self.center

    x0, y0 = p0
    x1, y1 = p1
    self.canvas.create_rectangle(
      x0 * UI_SCALE + cx,
      y0 * UI_SCALE + cy,
      x1 * UI_SCALE + cx,
      y1 * UI_SCALE + cy,
      varargs
    )

  def add_spacecraft(self, x, y, color):
    # colors = ["white", "blue", "red", "green"]
    index = 0
    fade = 0.5**index
    intensity = round(255.0*fade)
    intensity_hex = hex(intensity)[2:].zfill(2)
    fill_color = f'#{intensity_hex*3}'
    self.canvas.create_rectangle(
      (x - SPACE_SHIP_SIZE)* UI_SCALE + self.center[0],
      (y - SPACE_SHIP_SIZE)* UI_SCALE + self.center[1],
      (x + SPACE_SHIP_SIZE) * UI_SCALE + self.center[0],
      (y + SPACE_SHIP_SIZE) * UI_SCALE + self.center[1],
      width=0.25,
      # activefill=color,
      fill=color)

  def mainloop(self):
    self.root.mainloop()

  def draw_ships(self):
    if self.index >= len(self.responses):
      return
    state = self.responses[self.index].game_state
    for ship in state.ships:
      print (f"drawing {ship}")
      x, y = ship.position
      if ship.role == 0:
        color = "green"
      else:
        color = "blue"
      self.add_spacecraft(x, y, color)

  def draw(self):
    # clean canvas before draw
    self.canvas.delete(ALL)

    print (f"tick = {self.index + 1} (out of {len(self.responses)})")
    self.draw_gravity_field()
    self.draw_planet();
    self.draw_ships();

def main():
  responses = []
  with open("space-log.txt", 'r') as logs:
    for l in logs:
      l = l.strip('\n')
      ls = eval(l)
      print (ls)
      response = GameResponse.from_list(ls)
      responses.append(response)

  ui = SpaceUI(responses)
  ui.mainloop()
  
if __name__ == "__main__":
  main()