from datetime import datetime


def read_source(filename='galaxy.txt'):
  with open(filename, 'r') as galaxy_txt:
    program = galaxy_txt.read()
    return program.split('\n')


def parse_program(code_lines):
  # example code line:
  # ":1042 = ap ap cons 4 ap ap cons 63935 nil"
  #  ^       ^
  #  token   fn body
  defs = []
  for ln in code_lines:
    [token, body] = [chunk.strip() for chunk in ln.split('=')]
    operands = body.split()
    defs.append([ token, operands])
  return defs


def dump_file(strings, output_filename='decode_progress/galaxy_{suffix}.txt'):
  with open(output_filename.format(suffix=datetime.utcnow().isoformat()), 'w') as output:
    output.write('\n'.join(strings))

def sorted_defs(defs):
  return sorted(defs, key=lambda _def: len(_def[1]))

if __name__ == "__main__":
  defs = parse_program(read_source())
  for token, operands in sorted_defs(defs)[:48]:
    print(f'{token} = {" ".join(operands)}')

  sorted_strings = [f'{token} = {" ".join(operands)}' for token, operands in sorted_defs(defs)]
  dump_file(sorted_strings)
