import pageFetcher

channel = "UCSHozX8N-F7GygP9PIIYxLw"

fetcher = pageFetcher.Fetcher(channel)
print(fetcher.channelExists())
print(fetcher.channelID())
print(fetcher.hasCommunity())
print(fetcher.lastPage())

print(fetcher.fetchPage())
print(fetcher.fetchPage())
print(fetcher.fetchPage())
