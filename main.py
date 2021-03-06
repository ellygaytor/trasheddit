import argparse
import time
import os
import praw
from tqdm import tqdm
from auth import auth


parser = argparse.ArgumentParser(description="Shred a reddit account.")
parser.add_argument(
    "username", metavar="username", type=str, help="username to shred"
)
parser.add_argument(
    "-k",
    "--keep",
    metavar="keep",
    help="Keep submissions younger than the inputted time",
    default="0s",
)
parser.add_argument(
    "-o",
    "--overwrite",
    help="Overwrite submissions before deletion to prevent caching",
    action="store_true",
)
parser.add_argument(
    "-s",
    "--skip-subreddits",
    action="append",
    help="Subreddits to skip",
    required=False,
)
parser.add_argument(
    "-d",
    "--dry-run",
    help="Do not actually delete submissions",
    action="store_true",
)

args = parser.parse_args()

seconds_per_unit = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
    "M": 2629800,
    "y": 31557600,
}


def convert_to_seconds(s):
    """Convert the input into seconds using seconds_per_unit"""
    return float(s[:-1]) * seconds_per_unit[s[-1]]


def check_submission_date(submission_to_check):
    """Check if the passed in submission is past the cutoff"""
    now = time.time()
    cutoff = now - convert_to_seconds(args.keep)
    return submission_to_check.created_utc >= cutoff


def check_submission_subreddit(submission_to_check):
    """Check if the passed in submission is in a subreddit that should be skipped"""
    if args.skip_subreddits is not None:
        return (
            submission_to_check.subreddit.display_name in args.skip_subreddits
        )
    return None


reddit = auth(args.username)

if args.overwrite:
    reddit.validate_on_submit = True

# Stores submissions that have been checked and are safe to delete.
submissions = []

print("Getting and checking submissions...")
for comment in tqdm(
    (reddit.redditor(args.username).comments.new(limit=None)),
    desc="1000 most recent comments",
    unit=" comments",
):
    if (
        not check_submission_date(comment)
        and not check_submission_subreddit(comment)
        and not args.dry_run
    ):
        submissions.append(comment)

for post in tqdm(
    (reddit.redditor(args.username).submissions.new(limit=None)),
    desc="1000 most recent posts",
    unit=" posts",
):
    if (
        not check_submission_date(post)
        and not check_submission_subreddit(post)
        and not args.dry_run
    ):
        submissions.append(post)

# If overwrite is enabled, overwrite the comments and posts that are to be deleted.
if args.overwrite:
    print("Overwriting submissions...")
    # Edit the comments
    for submission in tqdm(submissions):
        submission.edit(os.urandom(1000).decode("latin1"))
    print("Waiting for edits to propagate (30 seconds)...")
    time.sleep(30)  # Sleep for 30 seconds to allow the edits to propagate.

# Delete the comments and posts
print("Deleting submissions...")
for submission in tqdm(submissions):
    submission.delete()
