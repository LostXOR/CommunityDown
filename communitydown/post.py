"""This is where the Post class is. That's pretty much all."""

import json
import requests
import communitydown

class Post:
    """Class representing a community post."""
    def __init__(self, data):
        """Parse and store raw post data as attributes of this object."""
        self.__raw_data = data
        self.__data = communitydown.parse_post_data(self.__raw_data)

    def data(self):
        """Return the parsed post data as a dict"""
        return self.__data

    def raw_data(self):
        """Return the raw post data as a dict"""
        return self.__raw_data

    def fetch_comments(self, chronological = False, limit = -1):
        """Fetches comments from this community post."""

        # Request more post information including continuation token to fetch comments
        params = self.raw_data()["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"] \
            ["publishedTimeText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["params"]
        request_data = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
            "browseId": self.data()["authorID"], "params": params
        }
        response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
            headers = {"Content-Type": "application/json"},
            data = json.dumps(request_data),
            timeout = 5)

        # Request first comments and some other data
        request_data["continuation"] = response.json()["contents"] \
            ["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"] \
            ["sectionListRenderer"]["contents"][1]["itemSectionRenderer"]["contents"][0] \
            ["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
        response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
            headers = {"Content-Type": "application/json"},
            data = json.dumps(request_data),
            timeout = 5)
        response_data = response.json()

        # Get exact comment count from response
        self.__data["commentCount"] = int(response_data["onResponseReceivedEndpoints"][0] \
            ["reloadContinuationItemsCommand"]["continuationItems"][0]["commentsHeaderRenderer"] \
            ["countText"]["runs"][0]["text"].replace(",", ""))

        # Return empty array if post has no comments
        if not "continuationItems" in response_data["onResponseReceivedEndpoints"][1] \
            ["reloadContinuationItemsCommand"]:
            return []

        # Get continuation token for correct comment sort (Top or Newest First)
        request_data["continuation"] = response_data["onResponseReceivedEndpoints"][0] \
            ["reloadContinuationItemsCommand"]["continuationItems"][0]["commentsHeaderRenderer"] \
            ["sortMenu"]["sortFilterSubMenuRenderer"]["subMenuItems"][int(chronological)] \
            ["serviceEndpoint"]["continuationCommand"]["token"]

        # Request comments until limit is hit or all comments are requested
        comments_data = []
        while limit == -1 or len(comments_data) < limit:
            # Request next batch of comments
            response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
                headers = {"Content-Type": "application/json"},
                data = json.dumps(request_data),
                timeout = 5)
            response_data = response.json()

            # First page
            if len(response_data["onResponseReceivedEndpoints"]) == 2:
                comments_data += response_data["onResponseReceivedEndpoints"][1] \
                ["reloadContinuationItemsCommand"]["continuationItems"]
            # Subsequent pages
            else:
                comments_data += response_data["onResponseReceivedEndpoints"][0] \
                ["appendContinuationItemsAction"]["continuationItems"]
            # Exit if last page
            if not "continuationItemRenderer" in comments_data[-1]:
                break

            # Grab continuation token
            request_data["continuation"] = comments_data.pop()["continuationItemRenderer"] \
            ["continuationEndpoint"]["continuationCommand"]["token"]

        # Limit was hit or last page was requested, so return comments up to limit
        if limit != -1 and len(comments_data) > limit:
            comments_data = comments_data[:limit]
        comments_data.reverse()
        return [communitydown.Comment(data) for data in comments_data]
