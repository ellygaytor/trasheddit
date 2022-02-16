import praw
import keyring
import json

def auth(username):

    account = keyring.get_password("trasheddit", username)
    if account is None:
        print(
            "No configuration found for '{}'. Please enter the PRAW configuration details now:".format(
                username
            )
        )
        client_id = str(input("client_id: "))
        client_secret = str(input("client_secret: "))
        username = username
        password = str(input("password: "))
        config = {
            client_id: client_id,
            client_secret: client_secret,
            username: username,
            password: password,
        }
        keyring.set_password("trasheddit", username, json.dumps(config))

    config = json.loads(account)

    reddit = praw.Reddit(
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret"),
        user_agent="trasheddit",
        username=config.get("username"),
        password=config.get("password"),
    )

    return reddit
