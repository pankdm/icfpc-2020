from modulate import modulate as mod
from parse_modulated import parse as dem
from send import do_send

def _modem(state):
  return dem(mod(state))

def _send(data):
  modulated = mod(data)
  print(f"Sending {data} as {modulated}")
  response = do_send(modulated)
  print(f"Got {response}")
  demodulated = dem(response)
  print(f"...parsed as {demodulated}")
  return demodulated

class Interactor:
  def __init__(self, draw_dot=None):
    self.draw_dot = draw_dot
    if not draw_dot:
      print("draw_dot is None, will print draw calls to stdout")

  def _draw(data):
    for (x, y) in data:
       if self.draw_dot:
         self.draw_dot(x, y)
       else:
         print(f"draw_dot({x}, {y})")

  def _multipledraw(data):
    if type(data) != "list":
      raise ValueError(f"multipledraw needs a list but got {data}")
    for item in data:
      self._draw(item)

  # https://message-from-space.readthedocs.io/en/latest/message38.html
  #
  # // list function call notation
  # f38 protocol (flag, newState, data) = if flag == 0
  #                 then (modem newState, multipledraw data)
  #                 else interact protocol (modem newState) (send data)
  # interact protocol state vector = f38 protocol (protocol state vector)
  # 
  # 
  # 
  # // mathematical function call notation
  # f38(protocol, (flag, newState, data)) = if flag == 0
  #                 then (modem(newState), multipledraw(data))
  #                 else interact(protocol, modem(newState), send(data))
  # interact(protocol, state, vector) = f38(protocol, protocol(state, vector))
  def f38(self, protocol, flag_newState_data):
  	(flag, newState, data) = tuple(flag_newState_data)
  	if flag == 0:
  		return [_modem(newState), self._multipledraw(data)]
  	else:
  		return self.interact(protocol, modem(newState), _send(data))

  def interact(self, protocol, state, vector):
  	return self.f38(protocol, protocol(state, vector))
