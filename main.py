import pageFetcher, parsePost

testChannel = "@CommunityDownTestChannel"
testChannelNoCommunity = "@CommunityDownTestNoCommunity"
testChannelEmpty = "@CommunityDownTestEmpty"

fetcher = pageFetcher.Fetcher(channel)
print(f"Channel exists: {fetcher.channelExists()}")
print(f"Channnel ID: {fetcher.channelID()}")
print(f"Channel has Community page: {fetcher.hasCommunity()}")
print(f"Last page of Community page: {fetcher.lastPage()}")

while not fetcher.lastPage():
    page = fetcher.fetchPage()
    for post in page:
        print(parsePost.parsePost(post))