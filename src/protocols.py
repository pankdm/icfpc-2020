from interact import *
from lists import *
from annotate import *
from funcs import *

STATELESSDRAW_CODE = "ap ap c ap ap b b ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c ap ap b cons ap ap c cons nil nil"
STATEFULDRAW_CODE = "ap ap b ap b ap ap s ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c cons nil ap c cons"

def simple_evaluator(code):
  tokens = code.split()
  return try_eval(expr_for_tokens(tokens), whitelist={})

def evaluator(expr, state, vector):
  assert(len(vector) == 2)
  print(f"expr = {expr}")  
  eval_result = AP(AP(expr, state), AP(AP(CONS, vector[0]), vector[1]))
  print(f"eval_result = {eval_result}")  
  return eval_result

# https://message-from-space.readthedocs.io/en/latest/message40.html
def statelessdraw(state, vector):
  print(f"statelessdraw {state} {vector}")
  return evaluator(simple_evaluator(STATELESSDRAW_CODE), state, vector)

# https://message-from-space.readthedocs.io/en/latest/message41.html
def statefuldraw(state, vector):
  print(f"statefuldraw {state} {vector}")
  return evaluator(simple_evaluator(STATEFULDRAW_CODE), state, vector)  

def main():
  (new_state, img_data) = interact(statefuldraw, NIL, [2, 3])
  print(f"new_state = {new_state} img_data={img_data}")

  multipledraw_helper(img_data)

if __name__ == "__main__":
  main()






