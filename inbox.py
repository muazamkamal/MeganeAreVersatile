import re
from praw.models.reddit.comment import Comment

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

        _, _, script, footer = db.info()

        for mentions in reddit.inbox.stream(skip_existing = True):
            # Only look for comments in inbox
            if type(mentions) == Comment:
                author = mentions.author
                message = mentions.body

                called = re.match(f"/?u/{bot.name}", message, re.IGNORECASE)
                delete = re.match(r"^delete$", message, re.IGNORECASE)

                if called:
                    # Reply when mentioned/tagged

                    # Skip if the submission is in the cache list
                    if str(mentions.submission.id) in db.cache_list():
                        continue

                    reply_message = script["en"] + footer
                    reply_comment = mentions.reply(reply_message)

                    # Cache the submission id
                    db.add_cache(str(mentions.submission.id))

                    log.log_response("comment", mentions.submission.id, reply_comment.id, mentions.id)
                elif delete:
                    # Delete the parent comment if requested for it

                    parent = mentions.parent()

                    if type(parent) == Comment and parent.author == bot:
                        parent.delete()

                        log.log_response("delete", mentions.submission.id, parent.id, mentions.id)