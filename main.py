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
parser.add_argument('-k', '--keep', metavar="keep", help='Keep submissions younger than the inputted time',
                    default="0s")
parser.add_argument('-s', '--skip-subreddits', action='append', help='Subreddits to skip', required=False)
parser.add_argument('-d', '--dry-run', help='Do not actually delete submissions', action="store_true")

args = parser.parse_args()

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "M": 2629800, "y": 31557600}


def convert_to_seconds(s):
    """Convert the input into seconds using seconds_per_unit"""
    return float(s[:-1]) * seconds_per_unit[s[-1]]


def check_submission_date(submission):
    """Check if the passed in submission is past the cutoff"""
    now = time.time()
    cutoff = now - convert_to_seconds(args.keep)
    return submission.created_utc >= cutoff


def check_submission_subreddit(submission):
    """Check if the passed in submission is in a subreddit that should be skipped"""
    if args.skip_subreddits is not None:
        return submission.subreddit.display_name in args.skip_subreddits


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
    if not check_submission_date(comment) and not check_submission_subreddit(comment) and not args.dry_run:
            comment.delete()

for post in tqdm((reddit.redditor(args.username).submissions.new(limit=None)), desc="1000 most recent posts",
                 unit=" posts"):
    if not check_submission_date(post) and not check_submission_subreddit(post) and not args.dry_run:
            post.delete()
