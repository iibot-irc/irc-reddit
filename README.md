irc-reddit
----------

An iibot plugin to get feed reddit posts into an IRC channel.

In your cron put a line like

    $HOME/bin/reddit "programming" "#mychannel" hot >/dev/null 2>&1

This will grab the "Hot" posts from `r/programming` and send them to #mychannel.

The state is maintained in `~/etc/reddit-SUBREDDITNAME-CHANNEL-storyids` *TODO* make that file not grow without bound.
