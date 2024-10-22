# No need for Brutus

## Description

<small>Author: @aenygma</small><br><br>A simple message for you to decipher: <br><br> <code>squiqhyiiycfbudeduutvehrhkjki</code> <br><br> Submit the original plaintext hashed with MD5, wrapped between the usual flag format: <code>flag{<hash_goes_here>}</code> <br><br> <small><i>Ex: If the deciphered text is "hello world", the MD5 hash would be <code>5eb63bbbe01eeed093cb22bb8f5acdc3</code>, and the flag would be <code>flag{5eb63bbbe01eeed093cb22bb8f5acdc3}</code>.</i></small>

## Solution

Rot 10

```
emit squiqhyiiycfbudeduutvehrhkjki |r.rot 10 |r.md5 -t
c945bb2173e7da5a292527bbbc825d3f
```
