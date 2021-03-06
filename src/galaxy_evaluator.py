# Usage:
#    python3 src/galaxy_evaluator.py galaxy.txt

import sys

# See video course https://icfpcontest2020.github.io/#/post/2054
class Expr:
    Evaluated = None

    def to_str(self):
      return str(self)

    def __repr__(self, *args, **krwargs):
      return self.to_str()


class Atom(Expr):
    Name = None

    def __init__(self, name):
        super().__init__()
        self.Name = name

    def to_str(self, *args, **krwargs):
        return str(self.Name)

class Val(Atom):
    Value = 0

    def __init__(self, value):
        super().__init__(str(value))
        self.Value = value
        self.Evaluated = self

    def to_str(self, *args, **krwargs):
        return self.Name

class Ap(Expr):
    Fun = None
    Arg = None

    @staticmethod
    def ap_equal(left, right):
        if type(left) != type(right):
            return False
        if isinstance(left, Atom) and isinstance(right, Atom):
           return left.Name == right.Name
        if type(left) == Ap and type(right) == Ap:
           return Ap.ap_equal(left.Fun, right.Fun) and Ap.ap_equal(left.Arg, right.Arg)

    def __init__(self, fun, arg):
        super().__init__()
        self.Fun = fun
        self.Arg = arg

    def to_str(self, max_depth=10, depth=None, *args, **krwargs):
        if max_depth is not None:
            depth = depth if depth is not None else 0
            if depth > max_depth:
                return f'ap ... ...'
            return f'ap {self.Fun.to_str(max_depth, depth+1)} {self.Arg.to_str(max_depth, depth+1)}'
        else:
            return f'ap {self.Fun.to_str(None)} {self.Arg.to_str(None)}'

    def to_padded_str(self, max_depth=10, depth=None, pad_with=' ', *args, **krwargs):
        depth = 0 if depth is None else depth
        if max_depth and depth > max_depth:
            return f'ap ... ...'
        child_padding = pad_with*(depth+1)
        fun_repr = self.Fun.to_padded_str(max_depth, depth+1, pad_with) if type(self.Fun) == Ap else str(self.Fun)
        arg_repr = self.Arg.to_padded_str(max_depth, depth+1, pad_with) if type(self.Arg) == Ap else str(self.Arg)
        return f'ap\n{child_padding}{fun_repr}\n{child_padding}{arg_repr}'


cons = Atom("cons")
t = Atom("t")
f = Atom("f")
nil = Atom("nil")

functions = {}

def eval(expr: Expr) -> Expr :
    if expr.Evaluated:
        return expr.Evaluated
    initialExpr = expr
    while True:
        result = tryEval(expr)
        if (result == expr):
            initialExpr.Evaluated = result
            return result
        expr = result

def tryEval(expr: Expr) -> Expr:
    if expr.Evaluated:
        return expr.Evaluated
    if (isinstance(expr, Val)):
        return expr
    if (isinstance(expr, Atom) and expr.Name in functions):
        return functions[expr.Name]
    if (isinstance(expr,Ap)):
        fun = eval(expr.Fun)
        x = expr.Arg
        if (isinstance(fun, Atom)):
            if (fun.Name == "neg"): return Val(-asNum(eval(x)))
            if (fun.Name == "i"): return x
            if (fun.Name == "nil"): return t
            if (fun.Name == "isnil"): return Ap(x, Ap(t, Ap(t, f)))
            if (fun.Name == "car"): return Ap(x, t)
            if (fun.Name == "cdr"): return Ap(x, f)
        if (isinstance(fun, Ap)):
            fun2 = eval(fun.Fun)
            y = fun.Arg
            if (isinstance(fun2, Atom)):
                if (fun2.Name == "t"): return y
                if (fun2.Name == "f"): return x
                if (fun2.Name == "add"): return Val(asNum(eval(y)) + asNum(eval(x)))
                if (fun2.Name == "mul"): return Val(asNum(eval(y)) * asNum(eval(x)))
                if (fun2.Name == "div"): return Val(asNum(eval(y)) // asNum(eval(x)))
                if (fun2.Name == "lt"): return t if asNum(eval(y)) < asNum(eval(x)) else f
                if (fun2.Name == "eq"): return t if asNum(eval(y)) == asNum(eval(x)) else f
                if (fun2.Name == "cons"): return evalCons(y, x)
            if (isinstance(fun2, Ap)):
                fun3 = eval(fun2.Fun)
                z = fun2.Arg
                if (isinstance(fun3, Atom)):
                    if (fun3.Name == "s"): return Ap(Ap(z, x), Ap(y, x))
                    if (fun3.Name == "c"): return Ap(Ap(z, x), y)
                    if (fun3.Name == "b"): return Ap(z, Ap(y, x))
                    if (fun3.Name == "cons"): return Ap(Ap(x, z), y)
    return expr


def evalCons(a: Expr, b: Expr) -> Expr:
    res = Ap(Ap(cons, eval(a)), eval(b))
    res.Evaluated = res
    return res

def asNum(n: Expr) -> int:
    if (isinstance(n, Val)):
        return n.Value
    if (isinstance(n, Atom)):
        return int(n.Name)
    raise TypeError(f"{n} is not a number")

def isnil(value):
  return isinstance(value, Atom) and value.Name == "nil"

def isnum(value):
    try:
        _ = asNum(value)
        return True
    except:
        return False

class TokenStream:
  def __init__(self, vec):
    self.vec = vec
    self.index = 0

  def read(self):
    res = self.vec[self.index]
    self.index += 1
    return res

def parse_from_tokens(tokens) -> Expr :
  stream = TokenStream(tokens)
  expr = parse_next_expr(stream)
  return expr

def parse_next_expr(s) -> Expr :
  token = s.read()
  if token == "ap":
    fun = parse_next_expr(s)
    arg = parse_next_expr(s)

    return Ap(fun, arg)
  else:
    try:
      return Val(int(token))
    except:
      return Atom(token)

def read_source(filename='galaxy.txt'):
  with open(filename, 'r') as galaxy_txt:
    program = galaxy_txt.read()
    lines = program.split('\n')
    non_empty_lines = filter(lambda l: len(l), lines)
    return non_empty_lines

def parse_program(code_lines):
  defs = {}
  for ln in code_lines:
    [token, body] = [chunk.strip() for chunk in ln.split('=')]
    lexems = body.split()
    defs[token] = lexems
  return defs

def load_galaxy_from_source(filename):
  defs = parse_program(read_source(filename))
  for name, tokens in defs.items():
    functions[name] = parse_from_tokens(tokens)

def evaluate_galaxy(state, vector):
  print(f"# evaluate_galaxy state={state} vector={vector}")
  expr = Ap(Ap(Atom("galaxy"), state), vector)
  res = eval(expr)
  # print(res)
  return res

def main():
  sys.setrecursionlimit(10000)
  load_galaxy_from_source(sys.argv[1])
  click = Ap(Ap(cons, Val(0)), Val(0))
  result = evaluate_galaxy(nil, click)
  print(result)

if __name__ == "__main__":
  main()
