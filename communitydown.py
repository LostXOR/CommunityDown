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
    output = {
        # Author properties
        "authorID": post["authorEndpoint"]["browseEndpoint"]["browseId"],
        "authorDisplayName": post["authorText"]["runs"][0]["text"],
        "authorImageURL": "https:" + post["authorThumbnail"]["thumbnails"][-1]["url"],
        # Post properties
        "postID": post["postId"],
        "likeCount": 0,
        "likeCountText": "0",
        "commentCountText": "0",
        "timeText": post["publishedTimeText"]["runs"][0]["text"],
        # Post contents
        "contentText": "",
        # Attachment
        "attachment": None
    }

    # Like and comment counts
    likeCountString = post["actionButtons"]["commentActionButtonsRenderer"]["likeButton"]["toggleButtonRenderer"]["accessibilityData"]["accessibilityData"]["label"]
    output["likeCount"] = int("".join([c for c in likeCountString if c.isdigit()]))
    if "voteCount" in post:
        output["likeCountText"] = post["voteCount"]["simpleText"]
    if "text" in post["actionButtons"]["commentActionButtonsRenderer"]["replyButton"]["buttonRenderer"]:
        output["commentCountText"] = post["actionButtons"]["commentActionButtonsRenderer"]["replyButton"]["buttonRenderer"]["text"]["simpleText"]

    # Post text contents
    if "runs" in post["contentText"]:
        output["contentText"] = post["contentText"]["runs"][0]["text"]

    # Post has some sort of attachment
    if "backstageAttachment" in post:
        attachment = post["backstageAttachment"]
        # Single image
        if "backstageImageRenderer" in attachment:
            output["attachment"] = {
                "type": "image",
                "url": attachment["backstageImageRenderer"]["image"]["thumbnails"][-1]["url"]
            }
        # Multiple images
        elif "postMultiImageRenderer" in attachment:
            output["attachment"] = {
                "type": "multiImage",
                "urls": [o["backstageImageRenderer"]["image"]["thumbnails"][-1]["url"] for o in attachment["postMultiImageRenderer"]["images"]]
            }
        # Poll
        elif "pollRenderer" in attachment:
            output["attachment"] = {
                "type": "poll",
                "votesText": attachment["pollRenderer"]["totalVotes"]["simpleText"],
                "choices": [o["text"]["runs"][0]["text"] for o in attachment["pollRenderer"]["choices"]],
                "imageURLs": [o["image"]["thumbnails"][-1]["url"] for o in attachment["pollRenderer"]["choices"]] if "image" in attachment["pollRenderer"]["choices"][0] else None
            }
        # Video
        elif "videoRenderer" in attachment:
            output["attachment"] = {
                "type": "video",
                "ID": attachment["videoRenderer"]["videoId"],
                "thumbnailURL": attachment["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
                "title": attachment["videoRenderer"]["title"]["runs"][0]["text"],
                "descriptionSnippet": attachment["videoRenderer"]["descriptionSnippet"]["runs"][0]["text"],
                "authorDisplayName": attachment["videoRenderer"]["longBylineText"]["runs"][0]["text"],
                "authorID": attachment["videoRenderer"]["longBylineText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
                "timeText": attachment["videoRenderer"]["publishedTimeText"]["simpleText"],
                "lengthText": attachment["videoRenderer"]["lengthText"]["simpleText"],
                "viewCount": int("".join([c for c in attachment["videoRenderer"]["viewCountText"]["simpleText"] if c.isdigit()])),
                "viewCountText": attachment["videoRenderer"]["shortViewCountText"]["simpleText"]
            }

    return output
