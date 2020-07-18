
import sys
import re
from decode import parse_program, read_source, sorted_defs

from funcs import *

def sorted_by_id(defs):
  return sorted(defs.items(), key=lambda _def: _def[0])


def try_eval(expr):
  if expr.name.startswith(":"):
    raise RuntimeError("Dereferencing is not supported")
  if re.match('-?\d+', expr.name):
    return int(expr.name)
  if expr.name == "ap":
    left = try_eval(expr.args[0])
    right = try_eval(expr.args[1])
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


if __name__ == "__main__":
  sys.setrecursionlimit(10000)
  defs = parse_program(read_source(sys.argv[1]))
  sorted_defs = sorted_defs(defs)
  for name, tokens in sorted_defs:
    stream = TokenStream(tokens)
    expr = parse_next_expr(stream)
    dump = expr.dump()

    try:
      maybe_eval = try_eval(expr)
    except RuntimeError:
      maybe_eval = "???"
    print (f'{name} = {dump}')
    print (f'      {maybe_eval}')


