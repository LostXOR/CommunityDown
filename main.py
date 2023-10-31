"""CLI!"""
import sys
import argparse
import json

from channel import Channel

# Create parser for CLI arguments
parser = argparse.ArgumentParser(
    description = "A downloader for YouTube Community posts"
)
parser.add_argument("-c", "--channel", required = True,
    help = "The ID, username, or URL of the channel to export.")
parser.add_argument("-f", "--format", choices = ["json"], default = "json",
    help = "The format of the export. Currently only JSON is supported.")
parser.add_argument("-o", "--output", required = True,
    help = "The file to export to.")
parser.add_argument("-P", "--post-limit", default = -1, type = int,
    help = "The maximum number of posts to download. Defaults to all.")
parser.add_argument("-C", "--comment-limit", default = -1, type = int,
    help = "The maximum number of comments to download. Defaults to all.")
parser.add_argument("-S", "--comment-sort",
    choices = ["top", "chronological"], default = "top",
    help = "Whether to use top or chronological comment sorting.")
args = parser.parse_args()

# Get channel
print("Fetching channel...")
channel = Channel(args.channel)

if not channel.exists():
    print("Channel does not exist.")
    sys.exit()
if not channel.has_community():
    print("Channel does not have a Community page.")
    sys.exit()

export = []

# Fetch posts
print("Fetching posts from channel...")
posts = channel.fetch_posts(limit = args.post_limit)

# Fetch comments
if args.comment_limit != 0:
    print(f"Fetching comments for {len(posts)} posts...")
    print(f"0/{len(posts)}", end = "")
    COUNT = 0
    for post in posts:
        comments = post.fetch_comments(
            limit = args.comment_limit,
            chronological = args.comment_sort == "chronological")
        export.append(post.data())
        export[0]["comments"] = [c.data() for c in comments]
        COUNT += 1
        print(f"\r{COUNT}/{len(posts)}", end = "")
    print()

# Write export to file
print("Saving to file...")
with open(args.output, "w", encoding = "utf-8") as file:
    file.write(json.dumps({"posts": export}))
print(f"Export saved to {args.output}.")
