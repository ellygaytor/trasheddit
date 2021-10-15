import argparse
import pickle
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
args = parser.parse_args()

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
    comment.delete()

for post in tqdm((reddit.redditor(args.username).submissions.new(limit=None)), desc="1000 most recent posts",
                 unit=" posts"):
    post.delete()
