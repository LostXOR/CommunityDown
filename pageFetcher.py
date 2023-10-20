import requests, json, re

class Fetcher:
    def __init__(self, channel):
        # Attributes
        self.__channelExists = False
        self.__channelID = None
        self.__hasCommunity = False
        self.__lastPage = True

        # Attempt to get channel page
        if channel.startswith("@"):
            response = requests.get("https://youtube.com/" + channel)
        elif "youtube.com" in channel:
            response = requests.get(channel)
        else:
            response = requests.get("https://youtube.com/channel/" + channel)

        # Check whether channel exists and has a Community tab
        if "/channel/" in response.text:
            self.__channelExists = True
            self.__channelID = re.findall('(?<=\/channel\/).*?(?=")', response.text)[0]
        if '"title":"Community"' in response.text:
            self.__hasCommunity = True
            self.__lastPage = False

        # Generate JSON data sent in POST to request community pages
        # params is a magic string that's used to get the community tab, no idea what it's for
        self.__nextRequestData = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": self.__channelID, "params": "Egljb21tdW5pdHnyBgQKAkoA"
        }

    # Functions to get attributes of Fetcher objects
    def channelExists(self):
        return self.__channelExists
    def hasCommunity(self):
        return self.__hasCommunity
    def lastPage(self):
        return self.__lastPage
    def channelID(self):
        return self.__channelID

    def fetchPage(self):
        if self.__lastPage:
            return []
        # Request community page from the API
        response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
        headers = {"Content-Type": "application/json"}, data = json.dumps(self.__nextRequestData))
        responseJSON = response.json()

        # First page of community posts
        if "contents" in responseJSON:
            tabs = responseJSON["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][:-1]
            communityTab = [tab for tab in tabs if tab["tabRenderer"]["title"] == "Community"][0]
            communityPosts = communityTab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

        # Subsequent pages
        elif "onResponseReceivedEndpoints" in responseJSON:
            communityPosts = responseJSON["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]

        # No community posts on channel
        if "messageRenderer" in communityPosts[0]:
            self.__lastPage = True
            return []

        # Check if this is last page and return
        if "backstagePostThreadRenderer" in communityPosts[-1]:
            self.__lastPage = True
            return communityPosts

        # Pop last "post" (a dummy post) from list and extract the continuation token
        # Continuation token is a magic string we need to send the API to get the next page
        contPost = communityPosts.pop()
        contToken = contPost["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
        self.__nextRequestData["continuation"] = contToken
        return communityPosts
