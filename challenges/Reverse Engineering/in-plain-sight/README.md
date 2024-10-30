# In Plain Sight

## Description

<small>Author: @JohnHammond, @Nordgaren</small><br><br>We found some malware, but it deleted itself before we could get ahold of it. It left this executable behind, though. It seems like a normal program, but the malware definitely was doing <i><b>something</b></i> with this binary. Can you find out what?<br><br>This kind of camouflage is just pure evil.  <br><br> <b>Download the file(s) below.</b> 


## Files

* [in_plain_sight](<files/in_plain_sight>)

## Solution

This challenge is another rust binary, similar to `rusty-bin`, but this one utilizes a much more complicated string encryption/lookup table technique.

I'm not going to pretend to understand what is happening fully, but this is what I gathered from my analysis:
* There are 9 PE resources of interest. the first 8 contain "state" information and the last one contains the icon, which also stores the encrypted strings.
* When a string is to be looked up, a state is initialized by parsing the PE resources, the state defines a, XOR keystream at a given point in time. The key stream is created by jumping around the different PE resources.
    * After generating the initial state, the algorithm continuously shuffles the state as it loops through bytes in the PNG file. It shuffles the state until it hits a known value that it is checking for.
* After the state has been shuffled, then the next thing in the state to be decrypted is a string.

Somebody pointed out that it was apparently possible to solve this challenge simply by modifying control flow to another "case" after shuffling in what appears to be a horibly mangled switch statement. I did not verify this, but that would imply that the encrypted strings are not dependent on the state of the keystream generation/the keystream always generates to a deterministic point. That, or I fundamentally misunderstand this challenge.

Anyways, after staring at the PNG parser and state manager for hours, I ended up noticing the hardcoded checks for `0xAAAAAA`, etc. I eventually just made a script to brute force these values and got somewhat lucky.


The lookup value that mapped to the string of interest was `0x10101010`, and the string was a malware config containing a list of IP addresses. The least significant octet in each IP could be converted to a character, and the ordering of the characters was based on the 3rd octet value.

```python
import sys
import subprocess
import os

os.makedirs("bins", exist_ok=True)
os.makedirs("bins\\output", exist_ok=True)

with open(sys.argv[1], "rb") as f:
    data = bytearray(f.read())

def patch(id, shash, data):

    with open(f"bins\\{id}.exe", "wb") as f:
        f.write(data[:0x1e90+4])
        f.write(shash.to_bytes(4, 'little'))
        f.write(data[0x1e90+8:])

    
    p = subprocess.Popen([f"bins\\{id}.exe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout_data = p.communicate(input="password12345\n\n\n\n")[0]
    print(hex(shash))
    print(stdout_data)
    return stdout_data

def worker(id, shash, ehash, data):
    for i in range(ehash-shash):
        patch(id, shash+i, data)

hash_groups = [
    (0x00, 0xFF),
]

# Try all the other A 4 byte values
patch(1, 0xAAA, data)
patch(1, 0xAAAA, data)
patch(1, 0xAAAAA, data)
patch(1, 0xAAAAAA, data)
patch(1, 0xAAAAAAA, data)
patch(1, 0xAAAAAAAA, data)

# Try their decimal representation as hex
patch(1, 0x1010, data)
patch(1, 0x101010, data)
patch(1, 0x10101010, data)

# Try some other random funny numbers
patch(1, 1337, data)
patch(1, 9001, data)
patch(1, 12345, data)
patch(1, 0x73736170, data) # pass in LE hex
patch(1, 0x70617373, data) # pass in BE hex

# Brute force 1 byte
work_set = 0
worker(1, hash_groups[work_set][0], hash_groups[work_set][1], data)
```