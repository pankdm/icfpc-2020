import sys
import io


def parse(f):
    # start = f.index
    prefix = f.read(2)
    if prefix == "":
        return None
    elif prefix == "00":
        return None
    elif prefix == "11":
        res1 = parse(f)
        res2 = parse(f)
        # print (f"current slice: {f.slice(start, f.index)}")
        # print (f"parsed {res1}")
        # print (f"parsed {res2}")
        return [res1, res2]
    else:
        num_bits = 0
        while True:
            bit = f.read(1)
            if bit == "0":
                break
            num_bits += 1
        if num_bits == 0:
            return 0
        number = f.read(4 * num_bits)
        if prefix == "01":
            sign = 1 
        else:
            sign = -1
        result = sign * int(number, 2)
        # print (f"parsed slice {f.slice(start, f.index)} as {result}")
        return result


class StringStream:
  def __init__(self, s):
    self.s = s
    self.index = 0

  def slice(self, start, end):
    return self.s[start : end]

  def peek(self, num):
    res = self.s[self.index : self.index + num]
    return res

  def read(self, num):
    res = self.s[self.index : self.index + num]
    self.index += num
    return res

if __name__ == "__main__":
    from player import flatten_cons
    for line in sys.stdin:
        line = line.strip('\n')
        print ("read", line)
        
        f = StringStream(line)
        res = parse(f)
        print ("parsed -> {}".format(res))
        print (f"flattened: {flatten_cons(res)}")


