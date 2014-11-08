#!/usr/bin/env python3

import sys,requests,json

REDDIT=sys.argv[1]
CHANNEL=sys.argv[2]
FEED=sys.argv[3]
# Test mode:
if len(sys.argv) == 5:
  sys.stderr.write("running in test mode\n")
  data = json.loads(open(sys.argv[4]).read())
else:
  req = requests.get("http://www.reddit.com/r/%s/%s.json" %(REDDIT,FEED), headers={'User-agent': 'iibot/irc-reddit'})
  if req.status_code != 200:
    print("mcpherrin: Kabloom!", req.text)
    sys.exit(1)
  data = req.json()

STATEFILE="/home/ircbot/state/reddit-%s-%s-storyids"%(CHANNEL,REDDIT)
sf = open(STATEFILE)
seen = set(sf.read().split("\n"))
sf.close()

for post in reversed(data["data"]["children"]):
  post = post['data']
  if not post["id"] in seen:
    id = post["id"]
    with open(STATEFILE, "a") as f:
      f.write(id + "\n")
    title = post["title"]
    url = post["url"]
    if post["domain"] == "self.%s" % REDDIT:
      print("/r/%s %s http://redd.it/%s/\n" % (REDDIT, title, id))
    else:
      print("/r/%s %s %s http://redd.it/%s\n" % (REDDIT, title, url, id))
