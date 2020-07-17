import math
def modulate(val):
    if val == None:
        return ""

    if val == []:
        return "00"

    is_number = type(val) == int
    res = ""
    if is_number:
        sign_bits = "01" if val >= 0 else "10"
        res += sign_bits
        res += modulate_num(abs(val))

    elif type(val) == list:
        res = "11"
        res += modulate(val[0])
        res += modulate(val[1:])     

    else:
        raise ValueError("Not implemented")
    

    return res

def modulate_num(val):
    if (val < 0):
        raise ValueError(f"Got {val} expected to get only positives here")

    res = ""
    unary_digs = math.ceil(val.bit_length() / 4)
    res += "1" * unary_digs

    if (unary_digs > 0):
        res += "0"

    res += format(abs(val), f"0{unary_digs*4}b")
    return res