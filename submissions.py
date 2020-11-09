import re

import helpers.firebase as database
from helpers.reddit import login
from helpers.data import load_data
import helpers.logger as logger

if __name__ == "__main__":
    db = database.Database()
    log = logger.Logger(db)

    reddit_creds = db.reddit_cred()
    reddit = login(reddit_creds)

    if reddit:
        bot = reddit.user.me()

        target_sub, trigger, script, footer = db.info()

        subreddit = reddit.subreddit(target_sub)

        for submission in subreddit.stream.submissions(skip_existing = True):
            title = submission.title

            found = re.search(trigger, title, re.IGNORECASE)

            # Reply to submission with trigger word included
            if found:
                # Skip if the submission is in the cache list
                if str(submission.id) in db.cache_list():
                    continue

                reply_message = script["en"] + footer
                reply_comment = submission.reply(reply_message)

                # Cache the submission id
                db.add_cache(str(submission.id))

                log.log_response("submission", submission.id, reply_comment.id)
