# NOTE: you need to install Python 3 from Python.org manually to run this on Mac.
# The default Python 3 doesn't include Tkinter bindings.

from tkinter import *
from models import *

UI_SCALE=3


# in pixels
SPACE_SHIP_SIZE = 2

def get_ship_color(ship):
  if ship.role == 0:
    return "orange"
  else:
    return "cyan"


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
    green = "#3CB043"
    varargs = {"fill": green}

    left = -48
    right = 48
    step = 32
    for cc in [-48, 48]:
      self.draw_line(cc, left, cc, right, **varargs)
      self.draw_line(left, cc, right, cc, **varargs)
    
    coords = [(-48, -16), (48, 16)]
    for a, b in coords:
      self.draw_line(a, -a, b, -b, **varargs)
      self.draw_line(a, a, b, b, **varargs)
      

  def draw_line(self, x0, y0, x1, y1, **varargs):
      self.canvas.create_line(
        self.map_x_coord(x0),
        self.map_y_coord(y0),
        self.map_x_coord(x1),
        self.map_y_coord(y1), 
        varargs)


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
      self.add_spacecraft(x, y, get_ship_color(ship))

  def draw_actions(self):
    if self.index >= len(self.responses):
      return
    state = self.responses[self.index].game_state
    for ship in state.ships:
      x, y = ship.position
      for command in ship.commands:
        if isinstance(command, ShootCommand):
          x_other, y_other = command.target
          self.draw_line(x, y, x_other, y_other, fill="red")
          self.draw_rectangular((x_other - 2, y_other - 2), (x_other + 2, y_other + 2), fill="red")

  def draw_ship_info(self):
    if self.index >= len(self.responses):
      return

    state = self.responses[self.index].game_state
    for (i, ship) in enumerate(state.ships):
      text = str(ship).replace(", commands=", ",\ncommands=")
      self.canvas.create_text(20, 20 + 40 * i, anchor=W, font="Monaco", text=text, fill=get_ship_color(ship))


  def draw(self):
    # clean canvas before draw
    self.canvas.delete(ALL)

    print (f"tick = {self.index + 1} (out of {len(self.responses)})")
    self.draw_gravity_field()
    self.draw_planet()
    self.draw_actions()
    self.draw_ships()
    self.draw_ship_info()

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