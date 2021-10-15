# trasheddit
Shred your reddit comment and post history

## Usage

### Simple Example

1. Download trasheddit: `git clone https://github.com/ellygaytor/trasheddit.git`
2. Change into its directory: `cd trasheddit`
3. Install its requirements: `pip3 install -r requirements.txt`
4. Run trasheddit: `python3 main.py`
5. Follow the prompts to generate a configuration file

Or, a one liner: 
```console
git clone https://github.com/ellygaytor/trasheddit.git && cd trasheddit && pip3 install -y -r requirements.txt && python3 main.py
```

### Options

| Option                      | Function                                        | Usage                                                                      |
|-----------------------------|-------------------------------------------------|----------------------------------------------------------------------------|
| `-k` or `--keep`            | Keep submissions younger than the inputted time | `-k 3M` will keep submissions younger than 3 months                        |
| `-s` or `--skip-subreddits` | Skip entered subreddits                         | `-s askreddit -s python` will skip submissions in r/askreddit and r/python |
| `d` or `--dry-run`          | Do a dry run                                    | `-d` will not actually delete any submissions                              |