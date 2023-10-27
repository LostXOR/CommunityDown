import requests, json
from parsepost import parsePost
from comment import Comment

class Post:
    def __init__(self, data):
        # Parse and store post data in this object
        self.rawData = data
        self.data = parsePost(self.rawData)
        for key in self.data:
            setattr(self, key, self.data[key])

    def fetchComments(self, newestFirst = False):
        # Request more post information including continuation token to fetch comments
        params = self.rawData["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]["publishedTimeText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["params"]
        requestData = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": self.authorID, "params": params
        }
        response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
        headers = {"Content-Type": "application/json"}, data = json.dumps(requestData))

        # Request first comments and some other data
        requestData["continuation"] = response.json()["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][1]["itemSectionRenderer"]["contents"][0]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
        response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
        headers = {"Content-Type": "application/json"}, data = json.dumps(requestData))
        responseData = response.json()

        # Return empty array if post has no comments
        if not "continuationItems" in responseData["onResponseReceivedEndpoints"][1]["reloadContinuationItemsCommand"]:
            return []

        # Get continuation token for correct comment sort (Top or Newest First)
        requestData["continuation"] = responseData["onResponseReceivedEndpoints"][0]["reloadContinuationItemsCommand"]["continuationItems"][0]["commentsHeaderRenderer"]["sortMenu"]["sortFilterSubMenuRenderer"]["subMenuItems"][int(newestFirst)]["serviceEndpoint"]["continuationCommand"]["token"]

        commentsData = []
        while True:
            # Request next batch of comments
            response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
            headers = {"Content-Type": "application/json"}, data = json.dumps(requestData))
            responseData = response.json()

            # First page
            if len(responseData["onResponseReceivedEndpoints"]) == 2:
                commentsData += responseData["onResponseReceivedEndpoints"][1]["reloadContinuationItemsCommand"]["continuationItems"]
            # Subsequent pages
            else:
                commentsData += responseData["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]
            # Return if last page
            if not "continuationItemRenderer" in commentsData[-1]:
                return [Comment(data) for data in commentsData]

            # Grab continuation token
            requestData["continuation"] = commentsData.pop()["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]