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
            for comment in submission.comments:
                if comment.is_submitter and comment.is_root:
                    if submission.author_flair_css_class in ["ocmaker", None, ""]:
                        if submission.author_flair_text and submission.author_flair_text.startswith("OC: "): # user already has an OC flair
                            oc_count = int(submission.author_flair_text.replace("OC: ","")) # get current flair and format it as an integer
                            oc_count += 1
                            newflair = "OC: {0}".format(oc_count)
                            reddit.subreddit('dataisbeautiful').flair.set(submission.author.name, newflair, "ocmaker") # set new flair
                        else: # user has never made an OC before
                            reddit.subreddit('dataisbeautiful').flair.set(submission.author.name, "OC: 1", "ocmaker") # set new flair
                    reply = 'Thank you for your [Original Content](https://www.reddit.com/r/dataisbeautiful/wiki/rules/rule3), /u/{0}!  \n**Here is some important information about this post:**\n\n* [View the author\'s citations](https://www.reddit.com{1})\n\n* [View other OC posts by this author](https://www.reddit.com/r/dataisbeautiful/search?q=author%3A\"{0}\"+title%3AOC&sort=new&include_over_18=on&restrict_sr=on)\n\nRemember that all visualizations on r/DataIsBeautiful should be viewed with a healthy dose of skepticism. If you see a potential issue or oversight in the visualization, please post a constructive comment below. Post approval does not signify that this visualization has been verified or its sources checked.\n\n[Join the Discord Community](https://discord.gg/NRnrWE7)\n\nNot satisfied with this visual? Think you can do better? [Remix this visual](https://www.reddit.com/r/dataisbeautiful/wiki/rules/rule3#wiki_remixing) with the data in the author\'s citation.\n\n---\n\n^^[I\'m&nbsp;open&nbsp;source](https://github.com/r-dataisbeautiful/dataisbeautiful-bot)&nbsp;|&nbsp;[How&nbsp;I&nbsp;work](https://www.reddit.com/r/dataisbeautiful/wiki/flair#wiki_oc_flair)'.format(submission.author.name,comment.permalink)
                    submission.reply(reply).mod.distinguish(sticky=True)
                    submission.save()
                    break
