import struct, sys, json

def load(path):
    data = open(path,'rb').read()
    n = struct.unpack_from('<I', data, 0)[0]
    offs = struct.unpack_from('<%dI'%(n+1), data, 4)
    ps = 4 + (n+1)*4
    strings = [data[ps+offs[i]:ps+offs[i+1]] for i in range(n)]
    rec_start = ps + offs[n]
    return data, n, strings, rec_start

if __name__ == '__main__':
    for path in sys.argv[1:]:
        data, n, strings, rs = load(path)
        print(f"{path.split('/')[-1]}: n={n}, pool=0x{4+(n+1)*4:x}..0x{rs:x}, rec_region=0x{rs:x}..0x{len(data):x} ({len(data)-rs} bytes)")
        # print first few strings and some key ones
        for i,s in enumerate(strings[:8]): print("  ",i,repr(s[:60]))
