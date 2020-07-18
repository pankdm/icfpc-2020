from datetime import datetime
from .funcs import FUNCTIONS, Ref, AP
import re

def read_source(filename='galaxy.txt'):
  with open(filename, 'r') as galaxy_txt:
    program = galaxy_txt.read()
    lines = program.split('\n')
    non_empty_lines = filter(lambda l: len(l), lines)
    return non_empty_lines


def read_test_source():
  return read_source('test_galaxy.txt')

def parse_program(code_lines):
  # example code line:
  # ":1042 = ap ap cons 4 ap ap cons 63935 nil"
  #  ^       ^
  #  token   fn body
  defs = {}
  for ln in code_lines:
    [token, body] = [chunk.strip() for chunk in ln.split('=')]
    lexems = body.split()
    defs[token] = lexems
  return defs

def parse_lexem(defs, lexem):
  if re.match(r'^-?\d', lexem):
    return int(lexem)
  elif lexem[0] == ':':
    return Ref(defs, lexem)
  elif lexem == 'ap':
    return AP()
  else:
    return FUNCTIONS.get(lexem, lexem)

def parse_program_with_types(code_lines):
  defs = parse_program(code_lines)
  defs_with_types = {}
  for token, lexems in defs.items():
    defs_with_types[token] = [ parse_lexem(defs_with_types, l) for l in lexems]
  return defs_with_types

def parse_program_with_ast(code_lines):
  defs = parse_program(code_lines)
  defs_with_ast = {}
  for token, lexems in defs.items():
    first_lexem, *other_lexems = lexems
    first_lexem = parse_lexem(defs_with_ast, first_lexem)
    if type(first_lexem) != AP:
      defs_with_ast[token] = first_lexem
    else:
      ast = AP()
      for l in other_lexems:
        ast.add_edge(parse_lexem(defs_with_ast, l))
      defs_with_ast[token] = ast
  return defs_with_ast

def dump_file(strings, output_filename='decode_progress/galaxy_{suffix}.txt'):
  with open(output_filename.format(suffix=datetime.utcnow().isoformat()), 'w') as output:
    output.write('\n'.join(strings))

def sorted_defs(defs):
  return sorted(defs.items(), key=lambda _def: len(_def[1]))

if __name__ == "__main__":
  defs = parse_program(read_source())
  for token, operands in sorted_defs(defs)[:48]:
    print(f'{token} = {" ".join(operands)}')

  sorted_strings = [f'{token} = {" ".join(operands)}' for token, operands in sorted_defs(defs)]
  dump_file(sorted_strings)

def usage():
  return '''
  `decode` usage:
    defs = parse_program(read_source())
    galaxy_lexems = defs['galaxy']
  '''
