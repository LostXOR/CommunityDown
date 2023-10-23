import requests, re, json

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

    def fetchPosts(self):
        # JSON data sent in POST to request community pages
        # params is a magic string that's used to get the community tab, no idea what it's for
        nextRequestData = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": self.__channelID, "params": "Egljb21tdW5pdHnyBgQKAkoA"
        }
        posts = []

        if not self.hasCommunity() or not self.exists():
            return None

        while True:
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
                posts = []
                return posts

            # Last page (return what we have)
            if "backstagePostThreadRenderer" in posts[-1]:
                return posts

            # Pop last "post" (a dummy post) from list (if we haven't hit the end) and extract the continuation token
            # Continuation token is a magic string we need to send the API to get the next page
            contPost = posts.pop()
            contToken = contPost["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
            nextRequestData["continuation"] = contToken

# Parse the raw post JSON returned by the API into a more friendly format by stripping non-essential data
# This function contains a lot of long JSON paths but there's really no way around that
def parsePost(post):
    # Get the data we really want
    post = post["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]
    output = {}

    # Author attributes
    output["authorID"] = post["authorEndpoint"]["browseEndpoint"]["browseId"] # ID of post author
    output["authorDisplayName"] = post["authorText"]["runs"][0]["text"] # Visible name of post author
    output["authorImage"] = "https:" + post["authorThumbnail"]["thumbnails"][-1]["url"] # Profile picture of post author

    # Post attributes
    output["postID"] = post["postId"] # Post ID
    likeCountString = post["actionButtons"]["commentActionButtonsRenderer"]["likeButton"]["toggleButtonRenderer"]["accessibilityData"]["accessibilityData"]["label"]
    output["likeCount"] = int("".join([c for c in likeCountString if c.isdigit()])) # Like count as a number
    output["likeCountText"] = post["voteCount"]["simpleText"] if "voteCount" in post else "0" # Like count in "pretty" text form
    output["timeText"] = post["publishedTimeText"]["runs"][0]["text"] # Time post was created in "pretty" text form
    # It seems the exact time the post was created is not returned by the API, so this is the best we have

    # Post comment count in text form (if post has comments)
    if "text" in post["actionButtons"]["commentActionButtonsRenderer"]["replyButton"]["buttonRenderer"]:
        output["commentCountText"] = post["actionButtons"]["commentActionButtonsRenderer"]["replyButton"]["buttonRenderer"]["text"]["simpleText"]
    else:
        output["commentCountText"] = "0"

    # Post has some sort of attachment
    if "backstageAttachment" in post:
        # Post image attachment(s)
        if "backstageImageRenderer" in post["backstageAttachment"]:
            output["images"] = [post["backstageAttachment"]["backstageImageRenderer"]["image"]["thumbnails"][-1]["url"]]
        elif "postMultiImageRenderer" in post["backstageAttachment"]:
            images = post["backstageAttachment"]["postMultiImageRenderer"]["images"]
            output["images"] = [o["backstageImageRenderer"]["image"]["thumbnails"][-1]["url"] for o in images]
        else:
            output["images"] = []

    return output