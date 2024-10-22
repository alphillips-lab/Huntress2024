# GoCrackMe2

## Description

<small>Author: @HuskyHacks</small><br><br>Not bad gophers, but that one was the easiest of the three! How will you do against something a little more involved? I wouldn't expect to get any help from debugging symbols on this one... <br><br> <b>Archive password: <code>infected</code></b> <br><br> <b>Download the file(s) below.</b>


## Files

* [GoCrackMe2.zip](<files/GoCrackMe2.zip>)

## Solution

This challenge is a Go binary with DWARF information removed, but symbols are still in tact in the `pclntab`. A tool like GoReSym can be used to recover the symbols on functions:

https://github.com/mandiant/GoReSym

This one generates a random number, and XOR decrypts a part of the stack containing the flag, but there's a random check (screenshot) that will quit early depending on a threshold.

![gocrackme2_1.png](/images/gocrackme2_1.png)

I solved this by patching the comparison with NOPs (`0x90`), and then running the binary again.