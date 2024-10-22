# GoCrackMe1

## Description

<small>Author: @HuskyHacks</small><br><br>TENNNNNN-HUT! 
<br><br> Welcome to the Go Dojo, gophers in training! 
<br><br> Go malware is on the rise. So we need you to sharpen up those Go reverse engineering skills. We've written three simple CrackMe programs in Go to turn you into Go-binary reverse engineering ninjas!
<br><br> First up is the easiest of the three. Go get em!
<br><br> <b>Archive password: <code>infected</code></b> <br><br> <b>Download the file(s) below.</b>


## Files

* [GoCrackMe1.zip](<files/GoCrackMe1.zip>)

## Solution

This crackme has a simple XOR loop that decodes the flag.

![gocrackme1_1.png](/images/gocrackme1_1.png)

```
emit '0:71-44coc``3dg0cc3c`nf2cno0e24435f0n+' |r.xor h:56
```