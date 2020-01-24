import praw
import os
import re

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     password=os.environ['ACCT_PASSWD'],
                     user_agent='r/dataisbeautiful bot (https://github.com/r-dataisbeautiful/dataisbeautiful-bot)',
                     username='dataisbeautiful-bot')

for submission in reddit.subreddit('dataisbeautiful').new(limit=100):
    if (re.search('[\[\(\{][oO][cC][\]\)\}]',submission.title) is not None) and (submission.link_flair_text is not "OC Approved") and (submission.approved_by is not None):
        submission.mod.flair(text="OC Approved",css_class="oc")

        if submission.author_flair_css_class in ["ocmaker", None, ""]: # ignore other flairs as to avoid overriding the "Practicioner", etc flairs
            if submission.author_flair_text.startswith("OC: "): # user already has an OC flair
                oc_count = int(submission.author_flair_text.replace("OC: ","")) # get current flair and format it as an integer
                oc_count += 1
                newflair = "OC: {0}".format(oc_count)
                reddit.subreddit('dataisbeautiful').flair.set(submission.author.name, newflair, "ocmaker") # set new flair
            else: # user has never made an OC before
                reddit.subreddit('dataisbeautiful').flair.set(submission.author.name, "OC: 1", "ocmaker") # set new flair
