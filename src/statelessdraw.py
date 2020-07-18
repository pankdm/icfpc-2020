from interact import *
from annotate import *
from funcs import *

# https://message-from-space.readthedocs.io/en/latest/message40.html
# statelessdraw = ap ap c ap ap b b ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c ap ap b cons ap ap c cons nil nil
def statelessdraw(state, vector):
  print(f"statelessdraw {state} {vector}")
  statelessdraw_code = "ap ap c ap ap b b ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c ap ap b cons ap ap c cons nil nil"
  # ap_code = ""
  tokens = statelessdraw_code.split()
  eval_result = try_eval(expr_for_tokens(tokens), whitelist={})
  print(f"eval_result = {eval_result}")
  run_result = eval_result.compute()(NIL)([1, 0])
  print(f"run_result = {run_result}")
  exit()
  return run_result

def main():
  interactor = Interactor()
  interactor.interact(statelessdraw, [], [1, 0])

if __name__ == "__main__":
  main()






