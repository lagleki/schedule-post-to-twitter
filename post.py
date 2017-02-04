import tweepy
import os
import re
import random
import codecs
from sys import argv, exit
import threading
import exrex

emptied = 0
header = "\n[from a secret #kuku arun]"
  
def GetTxt(fl):
    try:
        import codecs
        fileObj = codecs.open( fl, "r", "utf-8" )
        contents = fileObj.read().splitlines()
        if not contents:
            emptied = 1
        return contents
    except IOError:
        print('could not open file {0}'.format(fl))
        return

def rndm(contents):
        myline = random.choice(contents)
        return str(myline)
    
def postToTwitter(arrr,keys,output):
    msg = rndm(arrr)
    #To Twitter
    
    tweet = msg
    if len(msg) > 140 - len(header):
        tweet = msg[140 - len(header)]
    tweet = "%s%s" %(tweet,header)
    tweet = re.sub(r"\t","\n",tweet)
    ckey = keys[0]
    csecret = keys[1]
    atoken = keys[2]
    asecret = keys[3]
    
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    try:
        api = tweepy.API(auth)
        api.update_status(tweet)
    except tweepy.TweepError as e:
        print(e.reasons)
        return
    
    #internal
    print(msg)
    arrr.remove(msg)
    #write arrr to fl
    with open(fl,"w") as myfil:  
        myfil.write("\n".join(arrr))
    #append msg to out.txt
    with open(output, "a") as myfile:
        myfile.write(msg+"\n")


if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: {0} <file>".format(os.path.basename(argv[0])))
        exit(1)

    # get keys from file
    file = argv[1]
    keys = []
    if os.path.exists(file):
        with open(file, 'r') as keysFile:
            try:
                keys = keysFile.readlines()
                keys[:] = [key.replace('\n', '') for key in keys]
                keys[:] = [key.replace('\r', '') for key in keys]
 
            except IOError:
                print("Could not read file: ", file)
    else:
        print("file", file, "does not exist")
        exit(1)
        # destroy whole timeline
    def destroy():
        ckey = keys[0]
        csecret = keys[1]
        atoken = keys[2]
        asecret = keys[3]

        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        try:
            api = tweepy.API(auth)
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    api.destroy_status(status.id)
                except:
                    pass
        except:
            pass
          
    if len(argv) >= 2:
        fl = argv[2]
    else:
        fl = 'db.txt'
    if len(argv) >= 3:
        out = argv[3]
    else:
        out = 'out.txt'
    if len(argv) >= 5:
        destroy()
        exit("destroyed")
     #print ranMessage
    
    #multi send
    def setInterval(func, keys, sec,output):
        def func_wrapper():
            setInterval(func, keys, sec, output) 
            arrr = GetTxt(fl)
            func(arrr,keys,output)  
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
    setInterval(postToTwitter,keys,3,out)
    
    
    # one time send
    #arrr = GetTxt(fl)
    #postToTwitter(arrr,keys,out)

