from struct import unpack
from json import loads
from Crypto.Util.number import bytes_to_long as b2l


# Solve from unblvr
# https://discord.com/channels/1154524804947378186/1301984034506932284/1302781510868533361

def bxor(s1,s2): return b''.join(bytes([a ^ b]) for a,b in zip(s1,s2))

## First extract all the resource files using Resource Hacker or similar. There's 8 ICO files and 1 PNG

imgs = [ ("Icon1.ico", 16), ("Icon2.ico", 24), 
         ("Icon3.ico", 32), ("Icon4.ico", 48), 
         ("Icon5.ico", 64), ("Icon6.ico", 72), 
         ("Icon7.ico", 96), ("Icon8.ico", 128)
       ]

out = b""

for img, dim in imgs:
    tmp = open(img,"rb").read()[22:]
    hsize,width,height,_,_,_,size,_,_,_,_ = unpack("<"+"LLLHHLLLLLL", tmp[:40])
    image = tmp[40:40+size]
    mask = tmp[40+size:]
    bytes_per_mask = len(mask) // width
    shift = 8*bytes_per_mask - width
    
    mask = [b2l(mask[i:i+bytes_per_mask])>>shift for i in range(0, len(mask), bytes_per_mask)]
    mask = ''.join(format(e, f"0{width}b") for e in mask)
    chunks = [image[i:i+3] for i in range(0, len(image), 4)]
    out += b''.join(chunks[i] for i in range(len(mask)) if mask[i]=='1')


start = 216
skip = 1767
img = open("Icon9.ico","rb").read() # Actually a PNG
keystream = bxor(img, out)
data = bxor(keystream[start:], keystream[start+skip:])[:skip].decode()

json = loads(data[data.index("{"):data.index("}")+1])
ips = [list(map(int, ip.split("."))) for ip in json["ips"]]
ips.sort(key=lambda x:x[2])
print(bytes(ip[-1] for ip in ips)[:38].decode())