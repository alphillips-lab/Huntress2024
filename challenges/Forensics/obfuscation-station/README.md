# Obfuscation Station

## Description

<small>Author: @resume</small><br><br>You've reached the Obfuscation Station! <br>  Can you decode this PowerShell to find the flag? <br> <b>Archive password: <code>infected-station</code></b> <br><br> <b>Download the file(s) below.</b> 


## Files

* [Challenge.zip](<files/Challenge.zip>)

## Solution

This is standard PowerShell Base64, compressed data.

```
emit chal.ps1 |r.carve b64 -lt1 |r.b64 |r.zl
```

