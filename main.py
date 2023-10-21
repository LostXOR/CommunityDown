import communitydown, json

testChannel = "@CommunityDownTestChannel"

channel = communitydown.Channel(testChannel)
print(f"Channel exists: {channel.exists()}")
print(f"Channnel ID: {channel.channelID()}")
print(f"Channel has Community page: {channel.hasCommunity()}")

posts = channel.fetchPosts()
for post in posts:
    print(communitydown.parsePost(post))