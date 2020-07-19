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

    width = 330 * UI_SCALE
    height = 300 * UI_SCALE
    self.canvas = Canvas(self.root, width=width, height=height, bg='black')
    self.center = (width / 2, height / 2)

    self.canvas.bind("<Button-1>", self.handle_click)
    self.canvas.bind("<Key>", self.handle_key)
    self.canvas.pack()


    self.responses = responses
    self.index = 0


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
    index = 0
    fade = 0.5**index
    intensity = round(255.0*fade)
    intensity_hex = hex(intensity)[2:].zfill(2)
    fill_color = f'#{intensity_hex*3}'
    cx, cy = self.center
    self.canvas.create_rectangle(
      -16 * UI_SCALE + cx,
      -16 * UI_SCALE + cy,
      16 * UI_SCALE + cx,
      16 * UI_SCALE + cy,
      fill="white"
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

  def draw(self):
    # clean canvas before draw
    self.canvas.delete(ALL)

    self.draw_planet();

    state = self.responses[self.index].game_state
    for ship in state.ships:
      print (f"drawing {ship}")
      x, y = ship.position
      if ship.role == 0:
        color = "green"
      else:
        color = "blue"
      self.add_spacecraft(x, y, color)


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