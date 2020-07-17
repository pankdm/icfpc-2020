import sys
import io


def parse(f):
    prefix = f.read(2)
    if prefix == "":
        return None
    elif prefix == "00":
        return []
    elif prefix == "11":
        res1 = parse(f)
        res2 = parse(f)
        return [res1] + res2
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
        return sign * int(number, 2)


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip('\n')
        print ("read", line)
        f = io.StringIO(line)
        res = parse(f)
        print ("parsed -> {}".format(res))


