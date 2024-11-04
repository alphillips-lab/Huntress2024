import refinery.shell as r
import sys
import struct

fdata = r.ef(sys.argv[1]) | ...

# Get the resources in a list
rcs = []
for rc in fdata | r.perc():
    rcs.append(rc)
rcs.pop(-1)
rcs.pop(-1)

def get_table_and_png(resources):
    keystream = bytearray()
    png = bytearray()
    for rc in resources:

        if rc[0:4] == b"\x89PNG":
            png = rc
            continue

        # Header Len, width, and height of the image
        # size of the image, then the mask is the remaining bytes
        hl, w, h, _, _, _, imsize, _, _, _, _ = struct.unpack("<IIIHHIIIIII", rc[0:0x28])

        # color size
        image = rc[hl:hl+imsize]
        mask = rc[hl+imsize:]

        mask_len = len(mask) // w
        cl = image | r.chop(w*4) | [bytearray]
        ml = mask | r.chop(mask_len) | [bytearray]

        for c, m in zip(cl, ml):
            for i in range(0, w):
                # For each bit in the mask, extend the
                # keystream with the RGB trio
                mask = m[i // 8] & 1 << (7 - (i % 8))
                if mask:
                    keystream.extend(c[i*4:i*4+3])
    
    output = keystream | r.xor(png) | ...
    assert output[:4] == b"HNTC"
    return output



table = get_table_and_png(rcs)

entries = []
table_len = struct.unpack("<I", table[4:8])[0]
for i in range(0, table_len*16, 16):
    entries.append(struct.unpack("<IIII", table[i+8:i+24]))

dec = {}
for dl, koff, doff, eid in entries:
    data = table[doff:doff+dl]
    key = table[koff:koff+dl]
    output = data | r.xor(key) | ...
    dec[eid] = output

for k, v in dec.items():
    print(f"Entry {k}: {v}")
