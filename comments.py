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

        # Load all relevant data
        target_sub, trigger, script, footer = db.info()

        # Target the specific subreddit
        subreddit = reddit.subreddit(target_sub)

        for comment in subreddit.stream.comments(skip_existing = True):
            author = comment.author
            message = comment.body

            # Skip if the message is by the bot itself
            if author == bot:
                continue

            found = re.search(trigger, message, re.IGNORECASE)

            # Only reply to message with the trigger word,
            # and length of lower than 900.
            # 951 is the shortest version of the copypasta
            if found and len(message) < 900:
                # Skip if the submission is in the cache list
                if str(comment.submission.id) in db.cache_list():
                    continue

                reply_message = script["en"] + footer
                reply_comment = comment.reply(reply_message)

                # Cache the submission id
                db.add_cache(str(comment.submission.id))

                log.log_response("comment", comment.submission.id, reply_comment.id, comment.id)