from src.decode import read_source, parse_program_with_ast
from src.funcs import *

# компиляция займет несколько секунд
# петон может отвалиться с ошибкой "maximum recursion depth exceeded while calling a Python object"
print('Compiling Galaxy AST')
defs_ast = parse_program_with_ast(read_source())
print('...done')

GALAXY = AP.calc(defs_ast['galaxy'])
GALAXY
