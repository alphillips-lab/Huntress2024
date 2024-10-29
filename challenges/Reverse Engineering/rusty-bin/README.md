# Rusty Bin

## Description

<small>Author: @JohnHammond, @Nordgaren</small><br><br>Is there a flag somewhere way down deep in this rusty bin? <br><br> <b>Download the file(s) below.</b> 


## Files

* [rusty_bin](<files/rusty_bin>)

## Solution

This file is a rust binary for Windows. The binary implements what appears to be a custom encrypted string lookup table, which is created from a structure that is decrypted from a PE resource.

At first, I just solved this by debugging because it was easier to see where things were happening. My approach was to find where the user input their data, then step up the call stack until I found something interesting. The main function of interest starts at `0x1400011A0`. This function initializes the custom string table, accepts the user input, checks the password, and outputs a random part of the flag if the user puts in the right password.

Here are some notable addresses:
- `0x140001D80` String table initializer
- `0x1400013A8` Make a call for user input
- `0x140001CB0` Get an item from the custom lookup table
- `0x1400019FA` Make a lookup for a random part of the flag from a subset of the flag
- `0x14000125F` Get the two ciphertexts from the PE resource and XOR them to get the lookup table.

I solved initially just by breaking on `0x1400019FA` and modifying the argument to pass it a lookup ID for a part of the flag. I went back and solved it statically as well.

Here is a solve script that does everything statically:
```python
import refinery.shell as r
import sys

from construct import (
    Struct,
    Int32ub,
    Int32ul,
    Array,
    this
)

# Get the encrypted resource from the file
encrypted_resource = r.emit(sys.argv[1]) | r.perc("RCDATA/100/1033") | ...

# Get the decrypted table from the resource
c1 = encrypted_resource | r.snip("248:828") | ...
c2 = encrypted_resource | r.snip("1076:1656") | ...

packed_table = c1 | r.xor(c2) | ...

binary_struct = Struct(
    "header" / Struct(
        "magic" / Int32ul,
        "count" / Int32ub,
    ),
    "table_items" / Array(
        this.header.count*2,
        Struct(
            "lookup_id" / Int32ul,
            "offset" / Int32ul,
            "length" / Int32ul,
        )
    )
)

# Parse the binary structure into something meaningful
table = binary_struct.parse(packed_table)
lookup = {}
for item in table.table_items:
    if item.lookup_id not in lookup:
        lookup[item.lookup_id] = [packed_table[item.offset:item.offset + item.length]]
    else:
        lookup[item.lookup_id].append(packed_table[item.offset:item.offset + item.length])

flag = ""
for k, item in sorted(lookup.items()):
    data = item[0] | r.xor(item[1]) | ...
    if k < 10:
        flag += data.decode()
    print(k, data)

print(flag)
```