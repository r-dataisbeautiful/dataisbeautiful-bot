import praw
import os
import re

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     password=os.environ['ACCT_PASSWD'],
                     user_agent='r/dataisbeautiful bot (https://github.com/r-dataisbeautiful/dataisbeautiful-bot)',
                     username='dataisbeautiful-bot')

for submission in reddit.subreddit('dataisbeautiful').new(limit=100):
    if (re.search('[\[\(\{][oO][cC][\]\)\}]',submission.title) is not None) and (submission.saved is False) and (submission.approved_by is not None):

        if submission.author_flair_css_class in ["ocmaker", None, ""]: # ignore other flairs as to avoid overriding the "Practicioner", etc flairs
            if submission.author_flair_text and submission.author_flair_text.startswith("OC: "): # user already has an OC flair
                oc_count = int(submission.author_flair_text.replace("OC: ","")) # get current flair and format it as an integer
                oc_count += 1
                newflair = "OC: {0}".format(oc_count)
                reddit.subreddit('dataisbeautiful').flair.set(submission.author.name, newflair, "ocmaker") # set new flair
            else: # user has never made an OC before
                reddit.subreddit('dataisbeautiful').flair.set(submission.author.name, "OC: 1", "ocmaker") # set new flair
            reply = 'Thank you for your [Original Content](https://www.reddit.com/r/dataisbeautiful/wiki/index#wiki_what_counts_as_original_content_.28oc.29.3F), /u/{0}!  \n**Here is some important information about this post:**\n\n* [View other OC posts by this author](https://www.reddit.com/r/dataisbeautiful/search?q=author%3A\"{0}\"+title%3AOC&sort=new&include_over_18=on&restrict_sr=on)\n\nNot satisfied with this visual? Think you can do better? [Remix this visual](https://www.reddit.com/r/dataisbeautiful/wiki/index#wiki_remixing) with the data in the in the author\'s citation.\n\n---\n\n^^[I\'m&nbsp;open&nbsp;source](https://github.com/r-dataisbeautiful/dataisbeautiful-bot)&nbsp;|&nbsp;[How&nbsp;I&nbsp;work](https://www.reddit.com/r/dataisbeautiful/wiki/flair#wiki_oc_flair)'.format(submission.author.name)
            submission.reply(reply).mod.distinguish(sticky=True)
            print(submission.permalink)
            submission.save()
