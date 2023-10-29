from channel import Channel

test_channel = "@CommunityDownTestChannel"

channel = Channel(test_channel)
print(f"Channel exists: {channel.exists()}")
print(f"Channnel ID: {channel.channel_id()}")
print(f"Channel has Community page: {channel.has_community()}")

posts = channel.fetch_posts()
for post in posts:
    print(post.contentText)
    comments = post.fetch_comments(chronological = True)
    print(comments)
