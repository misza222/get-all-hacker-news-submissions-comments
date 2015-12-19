Simple Python scripts to download all Hacker News submissions and comments and store them in a SQLite3 database, for use in ad-hoc data analysis.

This script uses the older [Algolia API](https://hn.algolia.com/api) for Hacker News (instead of the [official HN API](https://github.com/HackerNews/API)) due to its support for bulk requests and comment scores for most comments. Run-time of downloading and processing all Hacker News submissions is about 2 hours; run-time of downloading and processing all Hacker News comments is about 11 hours.

# TODO
  - if database already exists, simply fetch latests entried until that point

# Known Data Fidelity Caveats

Unfortunately, there are a few issues with the source data, which the scripts attempt to mitigate:

* Hacker News automatically converts certain punctuation in Submissions/Comments contain into stylistic unicode (e.g. "smart quotes") which cannot be stored in the database; the scripts will convert the punctuation back to UTF-8.
* Comments contain style and link HTML; the scripts attempt to strip it.
* On the server-side, there are gaps of missing submission and comment data before 2010.
* Comment scores are hidden server-size for comments after October 2014; this is coincidentally the month my blog post was published / the official API was published)
