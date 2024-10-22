# OceanLocust

## Description

<small>Author: @JohnHammond</small><br><br><i>Wow-ee zow-ee!!</i> Some advanced persistent threats have been doing some  tricks with hiding payloads in image files! <br><br> We thought we would try our hand at it too.  <br><br> <b>NOTE: this challenge includes a debug build of the binary used to craft the image, as well as a release build... so you may choose to go an easier route or a harder route ;)</b> <br><br> <b>Download the file(s) below.</b>


## Files

* [ocean_locust.7z](<files/ocean_locust.7z>)

## Solution

This archive contains an executable along with an image with a hidden message. Although reversing the binary is not required, you can figure out through forensic analysis of the image, or the binary, that there are chunks of data stored in various locations in the image. They are headed with `biT*` where `*` is an alphabetically increasing character starting with `a`. Through analysis, you can discern that these headers and the proceeding data can be XOR'd with each other to get chunks of the flag. XORing all of the chunks and concatenating them in their alphabetical order yields the flag.

I solved this manually, though CubeMastery shared a helpful solve script:

```python

f = open('./inconspicuous.png', 'rb')

PngSignature = b'\x89PNG\r\n\x1a\n'
if f.read(len(PngSignature)) != PngSignature:
    raise Exception('Invalid PNG Signature')

alphabet = b'abcdefghijklmnopqrstuvwxyz'

def xor(a,b):
    while len(a) < len(b):
        a+=b'b'
    ret = bytes([x^y for x,y in zip(a,b)])
    return ret

def read_chunk(f):
    # Returns (chunk_type, chunk_data)
    chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
    chunk_data = f.read(chunk_length)
    chunk_expected_crc, = struct.unpack('>I', f.read(4))
    chunk_actual_crc = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
    if chunk_expected_crc != chunk_actual_crc:
        raise Exception('chunk checksum failed')
    return chunk_type, chunk_data

chunks = []
while True:
    chunk_type, chunk_data = read_chunk(f)
    chunks.append((chunk_type, chunk_data))
    if chunk_type == b'IEND':
        break

prefix = b'biT'
alphabet = b'abcdefghijklmnopqrstuvwx'

chunks_ret = []

for c in alphabet:
    key = prefix + bytes([c])
    
    for chunk in chunks:
        if chunk[0] == key:
            chunks_ret.append((key, chunk[1]))
            break
    else:
        break

decoded = [xor(a[0], a[1]) for a in chunks_ret]

decoded = b''.join(decoded)
print(decoded)
```