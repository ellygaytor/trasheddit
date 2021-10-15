import argparse
import pickle
import time
from dataclasses import dataclass

import praw
from tqdm import tqdm


@dataclass
class PRAWConfig:
    """Class to store PRAW details"""
    client_id: str
    client_secret: str
    username: str
    password: str


parser = argparse.ArgumentParser(description='Shred a reddit account.')
parser.add_argument('username', metavar='username', type=str,
                    help='username to shred')
parser.add_argument('--keep', metavar="keep", default="0s")
parser.add_argument('--dry-run', action="store_true")

args = parser.parse_args()

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "M": 2629800, "y": 31557600}


def convert_to_seconds(s):
    return float(s[:-1]) * seconds_per_unit[s[-1]]


def check_submission_date(submission):
    now = time.time()
    cutoff = now - convert_to_seconds(args.keep)
    if submission.created_utc >= cutoff:
        return True
    else:
        return False


try:
    config = pickle.load(open(args.username + ".pickle", "rb"))
except (OSError, IOError) as e:
    print(
        "No configuration file found for '{}'. Please enter the PRAW configuration details now:".format(args.username))
    client_id = str(input("client_id: "))
    client_secret = str(input("client_secret: "))
    username = args.username
    password = str(input("password: "))
    config = PRAWConfig(client_id, client_secret, username, password)
    pickle.dump(config, open(args.username + ".pickle", 'wb'))

reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent="trasheddit",
    username=config.username,
    password=config.password
)

for comment in tqdm((reddit.redditor(args.username).comments.new(limit=None)), desc="1000 most recent comments",
                    unit=" comments"):
    if not check_submission_date(comment):
        if not args.dry_run:
            comment.delete()

for post in tqdm((reddit.redditor(args.username).submissions.new(limit=None)), desc="1000 most recent posts",
                 unit=" posts"):
    if not check_submission_date(post):
        if not args.dry_run:
            post.delete()
