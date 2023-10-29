"""You guessed it, the parse_comment function is here."""

def parse_comment(comment):
    """Parse the JSON data of comments returned by the API into something comprehensible."""
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
        "contentText": "",
    }
    # Like and reply counts
    like_count_string = comment["actionButtons"]["commentActionButtonsRenderer"]["likeButton"] \
        ["toggleButtonRenderer"]["accessibilityData"]["accessibilityData"]["label"]
    output["likeCount"] = int("".join([c for c in like_count_string if c.isdigit()]))
    if "replyCount" in comment:
        output["replyCount"] = comment["replyCount"]

    # Parse comment content ("reverse" formatting)
    for run in comment["contentText"]["runs"]:
        if "bold" in run:
            run["text"] = "*" + run["text"] + "*"
        if "italics" in run:
            run["text"] = "_" + run["text"] + "_"
        if "strikethrough" in run:
            run["text"] = "-" + run["text"] + "-"
        output["contentText"] += run["text"]

    return output
