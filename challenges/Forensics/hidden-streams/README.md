# Hidden Streams

## Description

<small>Author: Adam Rice (@adam.huntress)</small><br><br>Beneath the surface, secrets glide,<br> A gentle flow where whispers hide.<br> Unseen currents, silent dreams,<br> Carrying tales in hidden streams.<br> <br> Can you find the secrets in these Sysmon logs? <br><br> <b>Download the file(s) below.</b>


## Files

* [Challenge.zip](<files/Challenge.zip>)

## Solution

There is an entry with a hidden file stream, but you can also just look for Base64 data in the file:

```
emit Sysmon.evtx |r.carve b64 [| r.b64 | r.rex flag.* ] 
```
