# Base-p-

## Description

<small>Author: Izzy Spering</small><br><br>That looks like a weird encoding, I wonder what it's based on. <br><br> <b>Download the file(s) below.</b>


## Files

* [based.txt](<files/based.txt>)

## Solution

This file is Base65536 encoded, which is an esoteric encoding algorithm. There are several layers of encoding, which ultimately yield a PNG file, where each RGB value of each square can be convered in order to yield the characters of the flag.

To get to the PNG file (which can be loaded in GIMP for example), the following command can be used:

```
emit based.txt |r.b65536 |r.b64 |r.zl |r.dump file.png
```