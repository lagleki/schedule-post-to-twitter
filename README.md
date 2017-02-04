Get keys and tokens to your Twitter account and save them to key.txt separating by newline and in this order:

```
ckey
csecret
atoken
asecret
```

To start using messages from in.txt and posting them to Twitter and saving them to out.txt:

```
python post.py key.txt in.txt out.txt
```

Make sure in.txt is never empty or the script won't be able to post anything. In case in.txt is empty just add new lines to it.

To purge your Twitter account add the fourth argument (can be any value):

```
python post.py key.txt in.txt out.txt 1
```
