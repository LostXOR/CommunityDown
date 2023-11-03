"""Home to parse_post, and nothing else."""

def parse_post_data(post):
    """Parse the raw post JSON returned by the API into a more friendly format.
    Strips non-essential data and grabs only what we want.
    """

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
        "commentCount": None,
        "commentCountText": "0",
        "timeText": post["publishedTimeText"]["runs"][0]["text"].removesuffix(" (edited)"),
        "edited": post["publishedTimeText"]["runs"][0]["text"].endswith(" (edited)"),
        # Post contents
        "contentText": None,
        # Attachment
        "attachment": None
    }

    # Like and comment counts
    like_count_string = post["actionButtons"]["commentActionButtonsRenderer"]["likeButton"] \
        ["toggleButtonRenderer"]["accessibilityData"]["accessibilityData"]["label"]
    output["likeCount"] = int("".join([c for c in like_count_string if c.isdigit()]))
    if "text" in post["actionButtons"]["commentActionButtonsRenderer"] \
        ["replyButton"]["buttonRenderer"]:
        output["commentCountText"] = post["actionButtons"]["commentActionButtonsRenderer"] \
            ["replyButton"]["buttonRenderer"]["text"]["simpleText"]

    # Post text contents
    if "runs" in post["contentText"]:
        output["contentText"] = "".join([run["text"] for run in post["contentText"]["runs"]])

    # Post has some sort of attachment
    if "backstageAttachment" in post:
        attachment = post["backstageAttachment"]
        # Single image
        if "backstageImageRenderer" in attachment:
            output["attachment"] = {
                "type": "image",
                "URL": attachment["backstageImageRenderer"]["image"]["thumbnails"][-1]["url"]
            }
        # Multiple images
        elif "postMultiImageRenderer" in attachment:
            output["attachment"] = {
                "type": "multiImage",
                "URLs": [o["backstageImageRenderer"]["image"]["thumbnails"][-1]["url"]
                    for o in attachment["postMultiImageRenderer"]["images"]]
            }
        # Poll
        elif "pollRenderer" in attachment:
            output["attachment"] = {
                "type": "poll",
                "votesText": attachment["pollRenderer"]["totalVotes"]["simpleText"],
                "choices": [o["text"]["runs"][0]["text"]
                    for o in attachment["pollRenderer"]["choices"]],
                "imageURLs": None
            }
            if "image" in attachment["pollRenderer"]["choices"][0]:
                # This is a valid operation and doesn't error
                # pylint: disable-next=unsupported-assignment-operation
                output["attachment"]["imageURLs"] = [o["image"]["thumbnails"][-1]["url"]
                    for o in attachment["pollRenderer"]["choices"]]

        # Video
        elif "videoRenderer" in attachment:
            output["attachment"] = {
                "type": "video",
                "ID": attachment["videoRenderer"]["videoId"],
                "thumbnailURL": attachment["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
                "title": attachment["videoRenderer"]["title"]["runs"][0]["text"],
                "descriptionSnippet": attachment["videoRenderer"]["descriptionSnippet"] \
                    ["runs"][0]["text"],
                "authorDisplayName": attachment["videoRenderer"]["longBylineText"] \
                    ["runs"][0]["text"],
                "authorID": attachment["videoRenderer"]["longBylineText"] \
                    ["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
                "timeText": attachment["videoRenderer"]["publishedTimeText"]["simpleText"],
                "lengthText": attachment["videoRenderer"]["lengthText"]["simpleText"],
                "viewCount": int(attachment["videoRenderer"]["viewCountText"]["simpleText"]
                    .removesuffix(" views")
                    .replace(",", "")),
                "viewCountText": attachment["videoRenderer"]["shortViewCountText"]["simpleText"]
            }
        # Quiz
        elif "quizRenderer" in attachment:
            output["attachment"] = {
                "type": "quiz",
                "choices": [o["text"]["runs"][0]["text"]
                    for o in attachment["quizRenderer"]["choices"]],
                "correctChoice": [o["isCorrect"]
                    for o in attachment["quizRenderer"]["choices"]].index(True),
                "explanation": attachment["quizRenderer"]["choices"][0]["explanation"] \
                    ["runs"][0]["text"],
                "answerCountText": attachment["quizRenderer"]["totalVotes"]["simpleText"]
            }

    return output
