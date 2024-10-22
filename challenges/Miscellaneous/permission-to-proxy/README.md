# Permission to Proxy

## Description

<small>Author: @JohnHammond</small><br><br>Where do we go from here? <br><br> Escalate your privileges and find the flag in root's home directory. <br><br> <b>Yes, the error message you see on startup is intentional. ;)</b> <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

Permission to proxy was a live service requiring you to proxy through the service's Squid Proxy, then scan the localhost for open ports.

Modifying a tool such as `spose` to scan all ports was enough to find a new service on port `50000`.

https://github.com/aancw/spose

The service on `localhost:50000` executed what it received as bash commands, so you could send a malicious GET request to the service containing a bash command such as a reverse shell.

Upon obtaining a reverse shell, checking for SUID binaries showed that `bash` also had SUID permissions, which means it was a simple escalation to root.

```
find / -perm /2000 2>/dev/null

sudo bash -i
```