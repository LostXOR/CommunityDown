import requests, re, json
from post import Post

class Channel:
    def __init__(self, channel):
        # Attempt to get channel page
        if channel.startswith("@"):
            response = requests.get("https://youtube.com/" + channel)
        elif channel.startswith("https://"):
            response = requests.get(channel)
        elif "youtube.com" in channel:
            response = requests.get("https://" + channel)
        else:
            response = requests.get("https://youtube.com/channel/" + channel)

        # Check whether channel exists and has a Community tab
        self.__channelExists = False
        self.__hasCommunity = False
        self.__channelID = None
        if 'href="https://www.youtube.com/channel/' in response.text:
            self.__channelExists = True
            self.__channelID = re.findall('(?<=href="https:\/\/www\.youtube\.com\/channel\/).*?(?=")', response.text)[0]
        if '"title":"Community"' in response.text:
            self.__hasCommunity = True

    def exists(self):
        return self.__channelExists

    def hasCommunity(self):
        return self.__hasCommunity

    def channelID(self):
        return self.__channelID

    def fetchPosts(self, limit = 1):
        # JSON data sent in POST to request community pages
        # params is a magic string that's used to get the community tab, no idea what it's for
        nextRequestData = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": self.__channelID, "params": "Egljb21tdW5pdHnyBgQKAkoA"
        }
        posts = []

        if not self.hasCommunity() or not self.exists():
            return None

        while len(posts) < limit:
            # Request community page from the API
            response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
            headers = {"Content-Type": "application/json"}, data = json.dumps(nextRequestData))
            responseJSON = response.json()

            # First page of community posts (add to posts list)
            if "contents" in responseJSON:
                tabs = responseJSON["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][:-1]
                communityTab = [tab for tab in tabs if tab["tabRenderer"]["title"] == "Community"][0]
                posts += communityTab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

            # Subsequent pages (add to posts list)
            elif "onResponseReceivedEndpoints" in responseJSON:
                posts += responseJSON["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]

            # No community posts on channel (return empty)
            if "messageRenderer" in posts[0]:
                return []

            # Last page (return what we have)
            if "backstagePostThreadRenderer" in posts[-1]:
                # Reverse so posts are in chronological order
                posts.reverse()
                # Convert to Post objects and return
                return [Post(data) for data in posts]

            # Pop last "post" (a dummy post) from list (if we haven't hit the end) and extract the continuation token
            # Continuation token is a magic string we need to send the API to get the next page
            contPost = posts.pop()
            contToken = contPost["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
            nextRequestData["continuation"] = contToken

        # Limit was hit, so return posts up to limit
        posts = [Post(data) for data in posts[:limit]]
        posts.reverse()
        return posts