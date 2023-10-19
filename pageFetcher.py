import requests, json

class Fetcher:
    def __init__(self, channelID):
        self.__channelID = channelID
        # JSON data sent in POST to request community pages
        # params is a magic string that's used to get the community tab, no idea what it's for
        self.__nextRequestData = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": channelID, "params": "Egljb21tdW5pdHnyBgQKAkoA"
        }
        self.__lastPage = False

    def fetchPage(self):
        if self.__lastPage:
            return []
        # Request community page from the API
        response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
        headers = {"Content-Type": "application/json"}, data = json.dumps(self.__nextRequestData))

        # Get list of community posts from JSON response
        responseJSON = response.json()
        if "contents" in responseJSON:
            tabs = responseJSON["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][:-1]
            communityTab = [tab for tab in tabs if tab["tabRenderer"]["title"] == "Community"][0]
            communityPosts = communityTab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        elif "onResponseReceivedEndpoints" in responseJSON:
            communityPosts = responseJSON["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]

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
