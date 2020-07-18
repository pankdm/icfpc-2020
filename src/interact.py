from modulate import modulate as mod
from parse_modulated import parse as dem
from send import do_send
from lists import cons_list_to_py_list

def _send_to_alien_proxy(data):
  modulated = mod(data)
  print(f"Sending {data} as {modulated}")
  response = do_send(modulated)
  print(f"Got {response}")
  demodulated = dem(response)
  print(f"...parsed as {demodulated}")
  return demodulated

def draw_helper(functional_data, draw_dot_impl=None):
  data = cons_list_to_py_list(functional_data)
  for pt_data in data:
     pt = cons_list_to_py_list(pt_data)
     (x, y) = tuple(pt)
     if draw_dot_impl:
       draw_dot_impl(x, y)
     else:
       print(f"draw_dot({x}, {y})")

def multipledraw_helper(functional_data, draw_dot_impl=None):
  data = cons_list_to_py_list(functional_data)
  for item in data:
    draw_helper(item, draw_dot_impl=draw_dot_impl)

# https://message-from-space.readthedocs.io/en/latest/message38.html
def interact(protocol_evaluator, state, vector):
  res = protocol_evaluator(state, vector)

  # Note: res will be modulatable here (consists of cons, nil and numbers only)
  (flag, newState, data) = tuple(cons_list_to_py_list(res))
  print(f"flag={flag} newState={newState} data={data}")
  if flag == 0:
      return (newState, data)

  return interact(protocol_evaluator, newState, _send_to_alien_proxy(data))

