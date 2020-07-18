
import sys
from decode import parse_program, read_source, sorted_defs

ALL_DEFS = {}


class Expr:
  def __init__(self, name, args):
    self.name = name
    self.args = args

  def __repr__(self):
    return self.name

  def show(self, indent = 0):
    print("{}{}".format(" " * indent, self.name))
    for arg in self.args:
      arg.show(indent + 2)

  def evaluate(self, depth=0):
    if depth > 5:
      raise RuntimeError("Infinite recursion")
    print("{}evaluating {}, {}".format(" " * 2 * depth, self.name, self.args))
    if self.name == "ap":
      op0 = self.args[0]
      op1 = self.args[1]
      if op0.name == "f":
        return lambda y: y
      x0 = op0.evaluate(depth + 1)
      x1 = op1.evaluate(depth + 1)
      return x0(x1)
    elif self.name == "cons":
      return lambda x: lambda y: (x, y)
    elif self.name == "car":
      return lambda x: x[0]
    elif self.name == "cdr":
      return lambda x: x[-1]
    elif self.name == "f":
      return lambda x: lambda y: y
    elif self.name == "t":
      return lambda x: lambda x: x
    elif self.name.startswith(":"):
      expr = ALL_DEFS.get(self.name, None)
      return expr.evaluate(depth + 1)
    elif self.name.isdigit():
      return int(self.name)
    else:
      assert False, f"unimpleted op: {self.name}"
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
  for name, tokens in sorted_defs(defs):
    stream = TokenStream(tokens)
    expr = parse_next_expr(stream)
    ALL_DEFS[name] = expr
    print(f'Added {name} = {tokens}')

    expr.show()
    # ev = expr.evaluate()
    # print (ev)
    print()
    # import pdb; pdb.set_trace()

  galaxy = ALL_DEFS["galaxy"]
  res = galaxy.evaluate()
  print (res)
  # all_names = sorted(defs.keys())
  # for name in all_names:
  #   expr = ALL_DEFS[name]
  #   expr.evaluate()
  
