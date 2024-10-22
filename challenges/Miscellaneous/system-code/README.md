# System Code

## Description

<small>Author: Truman Kain</small><br><br>Follow the white rabbit.  <br><br> <b>NOTE: Bruteforce is permitted for this challenge instance if you feel it is necessary.</b> <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

System code was a live service requiring you to diff the JavaScript files sourced in the service with the tool that the service was based on: https://github.com/Rezmason/matrix

Upon diffing the config file, you may notice a list of "backup" characters specified in the service's config file.

![systemcode_1.png](/images/systemcode_1.png)

Creating a script that attempts each permutation of the characters in the "backup" character list will ultimately yield the flag as a response to the correct password.