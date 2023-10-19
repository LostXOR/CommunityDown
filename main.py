import pageFetcher

channel = "UCTkXRDQl0luXxVQrRQvWS6w"

fetcher = pageFetcher.Fetcher(channel)
print(fetcher.validChannel())
print(fetcher.fetchPage())
print(fetcher.fetchPage())
print(fetcher.fetchPage())
