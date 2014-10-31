#!/usr/bin/env python

import sys,requests,json

REDDIT=sys.argv[1]
CHANNEL=sys.argv[2]
FEED=sys.argv[3]
# Test mode:
if len(sys.argv) == 5:
  print "running in test mode"
  data = json.loads(open(sys.argv[4]).read())
  writer=sys.stdout
else:
  req = requests.get("http://www.reddit.com/r/%s/%s.json" %(REDDIT,FEED))
  if req.status_code != 200:
    print "Kabloom!"
    print req.text
    sys.exit(1)
  data = req.json()
  writer=open("/home/ircbot/irc/irc.mozilla.org/%s/in"%CHANNEL, "a")

STATEFILE="/home/ircbot/state/reddit-%s-%s-storyids"%(CHANNEL,REDDIT)
sf = open(STATEFILE)
seen = set(sf.read().split("\n"))
sf.close()

new=[]
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
  for new in new:
    f.write(new+"\n")
  f.close()
