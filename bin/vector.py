def cat(data):
    ret = ''
    for i in data[1::]:
        ret += i + data[0]
    return ret[0:-len(data[0])] if len(data[0]) != 0 else ret

def merge(a, b, separator = ' '):
    return [a[i] + separator + b[i] for i in range(len(a) if len(a) < len(b) else len(b))]

def listfy(var):
    return var if type(var) is list else [var]