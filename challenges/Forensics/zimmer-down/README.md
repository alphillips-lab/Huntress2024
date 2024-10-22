# Zimmer Down

## Description

<small>Author: @sudo_Rem</small><br><br>A user interacted with a suspicious file on one of our hosts.<br> The only thing we managed to grab was the user's registry hive.<br> Are they hiding any secrets?<br> <br><br> <b>Download the file(s) below.</b>


## Files

* [NTUSER.DAT](<files/NTUSER.DAT>)

## Solution

The intended way to solve this challenge is by using Eric Zimmerman's forensic toolkit: https://ericzimmerman.github.io/

However, it can also be solved by looking through the strings and noticing a weird filename:
```
VJGSuERgCoVhl6mJg1x87faFOPIqacI3Eby4oP5MyBYKQy5paDF.b62.lnk
```

Base62 Decoding this yields the flag.