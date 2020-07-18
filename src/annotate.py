
import sys
import re
import os
import time
from decode import parse_program, read_source, sorted_defs

from funcs import *

def sorted_by_id(defs):
  return sorted(defs.items(), key=lambda _def: _def[0])

def create_file(it):
  timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
  # datetime.utcnow().isoformat()
  # folder = "annotations/tmp/{}".format(timestamp)
  folder = "annotations/tmp"
  os.makedirs(folder, exist_ok=True)
  filepath = "{}/{:03d}.txt".format(folder, it)
  return open(filepath, 'w')

def try_eval(expr, whitelist):
  if expr.name.startswith(":"):
    maybe_eval = whitelist.get(expr.name, None)
    if maybe_eval:
      return maybe_eval
    raise RuntimeError("Dereferencing is not supported")
  if re.match('-?\d+', expr.name):
    return int(expr.name)
  if expr.name == "ap":
    left = try_eval(expr.args[0], whitelist)
    right = try_eval(expr.args[1], whitelist)
    return AP(left, right)
  else:
    func = FUNCTIONS.get(expr.name, None)
    assert func, f'Unknown func: {expr.name}'
    return func

  
class Expr:
  def __init__(self, name, args):
    self.name = name
    self.args = args

  def __repr__(self):
    return self.name

  def dump(self):
    if self.name == "ap":
      left = self.args[0].dump()
      right = self.args[1].dump()
      return f'({self.name} {left} {right})'
    else:
      return self.name


class TokenStream:
  def __init__(self, vec):
    self.vec = vec
    self.index = 0

  def read(self):
    res = self.vec[self.index]
    self.index += 1
    return res

def parse_next_expr(s):
  token = s.read()
  if token == "ap":
    x0 = parse_next_expr(s)
    x1 = parse_next_expr(s)
    expr = Expr("ap", [x0, x1])
    return expr
  return Expr(token, [])


def simplification(sorted_defs):
  whitelist = {}
  for it in range(10):
    current_whitelist = {}
    with create_file(it) as output:
      for name, tokens in sorted_defs:
        stream = TokenStream(tokens)
        expr = parse_next_expr(stream)
        dump = expr.dump()

        try:
          maybe_eval = try_eval(expr, whitelist)
          current_whitelist[name] = maybe_eval
        except RuntimeError:
          maybe_eval = "???"
        output.write(f'{name} = {dump}\n')
        output.write(f'      {maybe_eval}\n')
    whitelist.update(current_whitelist)


if __name__ == "__main__":
  sys.setrecursionlimit(10000)
  defs = parse_program(read_source(sys.argv[1]))
  sorted_defs = sorted_defs(defs)
  simplification(sorted_defs)


