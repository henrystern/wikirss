# Wikipedia RSS Feed

A scraper that converts the Wikipedia front page to a daily RSS feed.

## Python environment

The python environment is managed by [uv](https://docs.astral.sh/uv/getting-started/installation/).

Once uv is installed, create the environment by running:

```bash
uv sync
```

Then activate the environment with:

```bash
source .venv/bin/activate
```

If you are using vscode, set your python interpretor to `.venv/bin/python`.

## Usage

Wikipedia blocks requests that do not have a proper user-agent header. You can set the user-agent by creating a `.env` file with a `USER_AGENT` key. For example:

```
USER_AGENT=YourNameWikiFetcher/1.0 (personal, low-rate use; contact: yourname@email.com)
```

To run the scraper and generate the feed, run:

```bash
make update-feed
```

This will create or update `atom.xml` and `rss.xml` in `data/processed/`.

You can also run the scraper directly with:

```bash
uv run src/wikirss/scrape.py
```

You can use cron to update the feed automatically.