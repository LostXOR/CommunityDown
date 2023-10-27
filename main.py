from channel import Channel

testChannel = "@CommunityDownTestChannel"

channel = Channel(testChannel)
print(f"Channel exists: {channel.exists()}")
print(f"Channnel ID: {channel.channelID()}")
print(f"Channel has Community page: {channel.hasCommunity()}")

posts = channel.fetchPosts()
for post in posts:
    print(post.contentText)
    comments = post.fetchComments(newestFirst = True)
    print(comments)