# Base64by32

## Description

<small>Author: @JohnHammond</small><br><br>This is a dumb challenge. I'm sorry. <br><br> <b>Download the file(s) below.</b>


## Files

* [base64by32.zip](<files/base64by32.zip>)

## Solution

This challenge requires you to Base64 decode the input 32 times.

This can be done simply with the following script:
```
import refinery as r
import sys

with open(sys.argv[1], "rb") as f:
  data = f.read()

for _ in range(32):
  data = data | r.b64() | ...

print(data)
```