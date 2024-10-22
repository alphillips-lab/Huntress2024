# Sekiro

## Description

<small>Author: @HuskyHacks</small><br><br>お前はもう死んでいる <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

Sekiro was a live service similar to rock-paper-scissors, though you had to automate the gameplay because if you were too slow, the program would close the connection.

After some trial and error, you could discover all of the gameplay options and then just keep playing until you get the flag. It turns out that Sekiro expected you to win 12 times in a row.

Here is a `pwntools` script that can solve the challenge:

```python
from pwn import *
import sys

server = remote(sys.argv[1],sys.argv[2])

for i in range(12):
    server.recvuntil(b"Opponent move: ")
    line = server.recvline()
    print(line)
    server.recvuntil(b"Your move: ")
    if b"block" in line:
        server.sendline(b"advance")
    elif b"strike" in line:
        server.sendline(b"block")
    elif b"advance" in line:
        server.sendline(b"retreat")
    elif b"retreat" in line:
        server.sendline(b"strike")

server.interactive()
```