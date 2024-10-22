# Stack It

## Description

<small>Author: @sudo_Rem</small><br><br>Our team of security analysts recently worked through a peculiar Lumma sample.<br> The dentists helping us advised we floss at least twice a day to help out.<br> He also gave us this weird file. Maybe you can help us out.<br> <br><br> <b>Download the file(s) below.</b>


## Files

* [stack_it.bin](<files/stack_it.bin>)

## Solution

This file is a linux binary that writes the flag to the stack after doing some decoding. It is meant to break with the most obvious tool, `floss`.

Binary Refinery also has a working solution:
```
emit stack_it.bin | r.vstack 0x8049000
```