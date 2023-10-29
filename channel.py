import re
import json
import requests
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
        self.__channel_exists = False
        self.__has_community = False
        self.__channel_id = None
        if 'href="https://www.youtube.com/channel/' in response.text:
            self.__channel_exists = True
            self.__channel_id = re.findall('(?<=href="https:\/\/www\.youtube\.com\/channel\/).*?(?=")', response.text)[0]
        if '"title":"Community"' in response.text:
            self.__has_community = True

    def exists(self):
        return self.__channel_exists

    def has_community(self):
        return self.__has_community

    def channel_id(self):
        return self.__channel_id

    def fetch_posts(self, limit = -1):
        # JSON data sent in POST to request community pages
        # params is a magic string that's used to get the community tab, no idea what it's for
        next_request_data = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": self.__channel_id, "params": "Egljb21tdW5pdHnyBgQKAkoA"
        }
        # Channel doesn't exist or doesn't have a community page
        if not self.has_community() or not self.exists():
            return None

        # Request posts until limit is hit or all posts have been requested
        posts = []
        while limit == -1 or len(posts) < limit:
            # Request community page from the API
            response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
            headers = {"Content-Type": "application/json"}, data = json.dumps(next_request_data))
            response_json = response.json()

            # First page of community posts (add to posts list)
            if "contents" in response_json:
                tabs = response_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][:-1]
                community_tab = [tab for tab in tabs if tab["tabRenderer"]["title"] == "Community"][0]
                posts += community_tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

            # Subsequent pages (add to posts list)
            elif "onResponseReceivedEndpoints" in response_json:
                posts += response_json["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]

            # No community posts on channel (return empty)
            if "messageRenderer" in posts[0]:
                return []

            # Last page (exit with what we have)
            if "backstagePostThreadRenderer" in posts[-1]:
                break

            # Pop last "post" (a dummy post) from list (if we haven't hit the end) and extract the continuation token
            # Continuation token is a magic string we need to send the API to get the next page
            cont_post = posts.pop()
            cont_token = cont_post["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
            next_request_data["continuation"] = cont_token

        # Limit was hit or last page was requested, so return posts up to limit
        if limit != -1 and len(posts) > limit:
            posts = posts[:limit]
        posts.reverse()
        return [Post(post) for post in posts]
