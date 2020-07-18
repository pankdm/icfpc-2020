import sys

# See video course https://icfpcontest2020.github.io/#/post/2054
class Expr:
    def __init__(self):
        self.Evaluated = None

class Atom(Expr):
    def __init__(self, name):
        self.Name = name

class Ap(Expr):
    def __init__(self, fun, arg):
        self.Fun = fun
        self.Arg = arg

class Vect:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

cons = Atom("cons")
t = Atom("t")
f = Atom("f")
nil = Atom("nil")

functions = {}

# See https://message-from-space.readthedocs.io/en/latest/message39.html
state: Expr = nil
vector = Vect(0, 0)

# while(True):
#     click = Ap(Ap(cons, Atom(vector.X)), Atom(vector.Y))
#     (newState, images) = interact(state, click)
#     PRINT_IMAGES(images)
#     vector = REQUEST_CLICK_FROM_USER()
#     state = newState

# # See https://message-from-space.readthedocs.io/en/latest/message38.html
# def interact(state: Expr, event: Expr): # -> (Expr, Expr)
#     expr = Ap(Ap(Atom("galaxy"), state), event)
#     res = eval(expr)
#     # Note: res will be modulatable here (consists of cons, nil and numbers only)
#     flag, newState, data = GET_LIST_ITEMS_FROM_EXPR(res)
#     if (asNum(flag) == 0):
#         return (newState, data)
#     return interact(newState, SEND_TO_ALIEN_PROXY(data))

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
    if (isinstance(expr, Atom) and functions[expr.Name]):
        return functions[expr.Name]
    if (isinstance(expr,Ap)):
        fun = eval(expr.Fun)
        x = expr.Arg
        if (isinstance(fun, Atom)):
            if (fun.Name == "neg"): return Atom(-asNum(eval(x)))
            if (fun.Name == "i"): return x
            if (fun.Name == "nil"): return t
            if (fun.Name == "isnil"): return Ap(x, Ap(t, Ap(t, f)))
            if (fun.Name == "car"): return Ap(x, t)
            if (fun.Name == "cdr"): return Ap(x, f)
        if (isinstance(fun, Ap)):
            fun2 = eval(fun.Fun)
            y = fun.Arg
            if (isinstance(fun2,Atom)):
                if (fun2.Name == "t"): return y
                if (fun2.Name == "f"): return x
                if (fun2.Name == "add"): return Atom(asNum(eval(x)) + asNum(eval(y)))
                if (fun2.Name == "mul"): return Atom(asNum(eval(x)) * asNum(eval(y)))
                if (fun2.Name == "div"): return Atom(asNum(eval(y)) / asNum(eval(x)))
                if (fun2.Name == "lt"): return t if asNum(eval(y)) < asNum(eval(x)) else f
                if (fun2.Name == "eq"): return t if asNum(eval(x)) == asNum(eval(y)) else f
                if (fun2.Name == "cons"): return evalCons(y, x)
            if (isinstance(fun2,Ap)):
                fun3 = eval(fun2.Fun)
                z = fun2.Arg
                if (isinstance(fun3,Atom)):
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
    if (isinstance(n,Atom)):
        return int(n.Name)
    raise TypeError("not a number")

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

def main():
  sys.setrecursionlimit(10000)
  defs = parse_program(read_source(sys.argv[1]))
  for name, tokens in defs.items():
    functions[name] = parse_from_tokens(tokens)

  click = Ap(Ap(cons, Atom("0")), Atom("0"))
  expr = Ap(Ap(Atom("galaxy"), nil), click)
  res = eval(expr)
  print(res)

if __name__ == "__main__":
  main()