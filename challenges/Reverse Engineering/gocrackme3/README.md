# GoCrackMe3

## Description

<small>Author: @HuskyHacks</small><br><br>You've trained, you've failed, you've succeeded, you've learned. Everything you've done up to this point has prepared you for this moment. Don't let me down, Gopher. Don't let me down.  <br><br> <b>Archive password: <code>infected</code></b> <br><br> <b>Download the file(s) below.</b>


## Files

* [GoCrackMe3.zip](<files/GoCrackMe3.zip>)

## Solution

This crackme is slightly more difficult. It is obfuscated with `garble`, a common Go obfuscator.

https://github.com/burrowers/garble

For this challenge, there are a few checks for certain things in the main function, and the flag is incrementally generated. I patched these checks out with NOPs (`0x90`), and was able to successfully grab the flag.

CubeMastery shared an interesting programmatic solution for exactly the same thing I did manually:

```python
import gdb

ge = gdb.execute
parse = gdb.parse_and_eval

bps = [
    0x4F7D80, # set $al = 1
    0x4F7F19, # set $bl = 1
    0x4F7EC0, # just to check it out
]

for bp in bps:
    ge(f"b*{hex(bp)}")

ge("r")
try:
    while True:
        rip = int(parse("$rip"))
        if rip == bps[0]:
            ge("set $al = 1")
            ge("c")
        elif rip == bps[1]:
            ge("set $bl = 1")
            ge("c")
        else:
            break
except Exception as e:
    print(e)
```