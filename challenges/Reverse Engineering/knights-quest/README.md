# Knight's Quest

## Description

<small>Author: @HuskyHacks</small><br><br>An adventurer is YOU! Play Knight's Quest, beat the three monsters, and claim the flag! Very straightforward with no surprises,  no sir-ee, no surprises here lmao <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

This challenge was a live service with a download for a game. The game binary contains a password which needed to be sent to the server to receive the flag.

![knights_quest_1.png](/images/knights_quest_1.png)

I only downloaded the linux version of the binary, though all of them are written in Go.

My initial solution involved patching the binary such that the final boss' health and damage were equal to `1`, but the more elegant solution is to find the password generator code and implement a static solution.

The password generator code is in the main gameloop function, `0x00498CA8`.

A python reimplementation that creates the password is the following:

```python
p = "BODUAhkDMLj3ZM7cfo9UBlt1ANUBY7LnecdpghL8mgZYJs6bhonfMQzeDjspI4LQ"
out = bytearray()
for i in range(32):
    n = (ord(p[i]) ^ ord(p[i+32])) % 62;
    m = n + 65;
    if ( m > 90 ):
        if ( m >= 97 ):
            if ( m > 122 ):
                m = (n - 10)
        else:
            m = (n + 71)
    out.append(m)

print(out)
```

Then we could send the password with the command they gave us to get the flag:
```
curl -X POST -H "Content-Type: application/json" -d '{"password":"hmafgAhAalqmQABBOAZtP3OWFegsQDAB"}' http://challenge.ctf.games:32701//submit
```