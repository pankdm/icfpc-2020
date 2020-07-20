

import io


from send import do_send
from lists import *
from parse_modulated import parse as dem

modulated = "1101100101110111111111111111110010110001101011101101110001010100010010010010011110110111010100100"
modulated = "11011001011101111111111111111000111100000101100101000000000110101111010011000011010100100000"
response = do_send(modulated)

f = open("debug-log.txt", "w")
f.write(response)
f.close()

demodulated = dem(io.StringIO(response))
print(f"...parsed as {demodulated}")
as_expr = py_to_tree(demodulated)
print(f"as_expr {as_expr}")
