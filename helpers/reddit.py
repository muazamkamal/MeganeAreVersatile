import praw
from prawcore.exceptions import OAuthException

def login(creds, verbose = True):
    try:
        reddit = praw.Reddit(
            user_agent = creds["user_agent"],
            client_id = creds["client_id"],
            client_secret = creds["client_secret"],
            username = creds["username"],
            password = creds["password"]
        )

        name = reddit.user.me()

        if verbose:
            print(f"Connected as /u/{name}")
    except OAuthException as ex:
        print(ex)
        reddit = None

    return reddit