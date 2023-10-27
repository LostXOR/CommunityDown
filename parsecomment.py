# Parse the JSON data of comments returned by the API into something comprehensible
def parseComment(comment):
    # Get the comment data we actually want
    comment = comment["commentThreadRenderer"]["comment"]["commentRenderer"]

    output = {
        # Author properties
        "authorID": comment["authorEndpoint"]["browseEndpoint"]["browseId"],
        "authorDisplayName": comment["authorText"]["simpleText"],
        "authorImageURL": comment["authorThumbnail"]["thumbnails"][-1]["url"],
        # Comment properties
        "commentID": comment["commentId"],
        "likeCount": 0,
        "replyCount": 0,
        "timeText": comment["publishedTimeText"]["runs"][0]["text"].removesuffix(" (edited)"),
        "edited": comment["publishedTimeText"]["runs"][0]["text"].endswith(" (edited)"),
        # Comment text
        "contentText": comment["contentText"]["runs"][0]["text"],
    }
    # Like and reply counts
    likeCountString = comment["actionButtons"]["commentActionButtonsRenderer"]["likeButton"]["toggleButtonRenderer"]["accessibilityData"]["accessibilityData"]["label"]
    output["likeCount"] = int("".join([c for c in likeCountString if c.isdigit()]))
    if "replyCount" in comment:
            output["replyCount"] = comment["replyCount"]

    return output