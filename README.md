# CommunityDown
CommunityDown is a downloader for YouTube community pages. It is currently in early development and is only partially functional.

## Usage
```
usage: main.py [-h] -c CHANNEL [-f {json}] -o OUTPUT [-P POST_LIMIT]
                     [-C COMMENT_LIMIT] [-S {top,chronological}]

A downloader for YouTube Community posts

options:
  -h, --help            show this help message and exit
  -c CHANNEL, --channel CHANNEL
                        The ID, username, or URL of the channel to export.
  -f {json}, --format {json}
                        The format of the export. Currently only JSON is
                        supported.
  -o OUTPUT, --output OUTPUT
                        The file to export to.
  -P POST_LIMIT, --post-limit POST_LIMIT
                        The maximum number of posts to download. Defaults to
                        all.
  -C COMMENT_LIMIT, --comment-limit COMMENT_LIMIT
                        The maximum number of comments to download. Defaults
                        to all.
  -S {top,chronological}, --comment-sort {top,chronological}
                        Whether to use top or chronological comment sorting.
```

## TODO
- Refactor code into a Python module
- Write better documentation
- Add ability to fetch comment replies
- Add HTML option for export format
- Add more CLI options (exporting individual posts, comments, etc.)
