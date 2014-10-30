#!/usr/bin/env python

import sys,requests

REDDIT=sys.argv[1]
CHANNEL=sys.argv[2]
FEED=sys.argv[3]

STATEFILE="/home/ircbot/state/reddit-%s-%s-storyids"%(CHANNEL,REDDIT)
seen = set(open(STATEFILE).read().split("\n"))

data = requests.get("http://www.reddit.com/r/%s/%s.json" %(REDDIT,FEED)).json()
new=[]
writer=open("/home/ircbot/irc/irc.mozilla.org/%s/in"%CHANNEL, "a")
for post in data["data"]["children"]:
  post = post['data']
  if not post["id"] in seen:
    writer.write(post["title"]+"\n")
    if post["domain"] == "self.%s" % REDDIT:
      writer.write(post["url"]+"\n")
    else:
      writer.write(post["url"]+" "+post["permalink"]+"\n")
    new.append(post["id"])
if len(new) != 0:
  f = open(STATEFILE, "a")
  f.write("\n".join(new))
