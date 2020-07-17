
from decode import parse_program, read_source



class Expr:
  def __init__(self, name, args):
    self.name = name
    self.args = args

  def show(self, indent = 0):
    print("{}{}".format(" " * indent, self.name))
    for arg in self.args:
      arg.show(indent + 2)

  def evaluate(self):
    if self.name == "ap":
      x0 = self.args[0].evaluate()
      x1 = self.args[1].evaluate()
      return x0(x1)
    elif self.name == "cons":
      return lambda x: lambda y: (x, y)
    elif self.name == "car":
      return lambda x: x[0]
    elif self.name == "cdr":
      return lambda x: x[-1]
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
  defs = parse_program(read_source())
  for name, tokens in defs[:10]:
    stream = TokenStream(tokens)
    expr = parse_next_expr(stream)
    print(f'{name} = {tokens}')

    expr.show()
    ev = expr.evaluate()
    print (ev)
    print()
    # import pdb; pdb.set_trace()
