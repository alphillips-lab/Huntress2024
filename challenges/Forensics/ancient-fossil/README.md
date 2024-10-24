# Ancient Fossil

## Description

<small>Author: @JohnHammond</small><br><br>All things are lost to time... <br><br> <b>Download the file(s) below.</b><br>


## Files

* [ancient.fossil](<files/ancient.fossil>)

## Solution

This file is a "fossil" database containing a version history for the database (I think, I didn't care to research the file format that much).

Anyways, the flag can be obtained through the following:
```
binwalk -e ancient.fossil && grep -R "flag" .
```

It appears that changes are stored in compressed streams, so decompressing the right stream is enough to get what you need.

Here is a one-liner with refinery and binwalk, that doesn't leave any artifacts:

```
binwalk ancient.fossil |resplit h:0a [|rex "^\\d+"|pack -B 8 10| put off [| ef ancient.fossil |snip off: |zl |rex flag.* ]]
```