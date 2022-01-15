# trasheddit
Shred your reddit comment and post history (x89/Shreddit replacement)

## Usage

### Simple Example

1. Download trasheddit: `git clone https://github.com/ellygaytor/trasheddit.git`
2. Change into its directory: `cd trasheddit`
3. Install its requirements: `pip3 install -r requirements.txt`
4. Run trasheddit: `python3 main.py [username]`
5. Follow the prompts to generate a configuration file. See [Configuring Credentials](#configuring-credentials) for more info.

Or, a one liner: 
```console
git clone https://github.com/ellygaytor/trasheddit.git && cd trasheddit && pip3 install -y -r requirements.txt && python3 main.py [username]
```

⚠️ Remember to change `[username]` to your Reddit username

### Options

| Option                      | Function                                        | Usage                                                                      |
|-----------------------------|-------------------------------------------------|----------------------------------------------------------------------------|
| `-k` or `--keep`            | Keep submissions younger than the inputted time | `-k 3M` will keep submissions younger than 3 months                        |
| `-s` or `--skip-subreddits` | Skip entered subreddits                         | `-s askreddit -s python` will skip submissions in r/askreddit and r/python |
| `d` or `--dry-run`          | Do a dry run                                    | `-d` will not actually delete any submissions                              |


### Configuring Credentials

Trasheddit requires the following credential information:

- client_id
- client_secret
- password

The Reddit API requires that automation mechanisms utilize their own authentication mechanism, as well as the mechanism to access your specific user account. The   `password` should be the login password associated with the `username` that the script is being run with.

To obtain the client ID and secret, follow these steps (taken from 
[PRAW documentation](http://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application)):

1. Open your Reddit application preferences by clicking [here](https://www.reddit.com/prefs/apps/).
2. Add a new application. It doesn't matter what it's named, but calling it "shreddit" makes it easier to remember.
3. Select "script".
4. Redirect URL does not matter for script applications, so enter something like http://127.0.0.1:8080
5. Once created, you should see the name of your application followed by 14 character string. Enter this 14 character
   string as your `client_id`.
6. Copy the 27 character "secret" string into the `client_secret` field.
