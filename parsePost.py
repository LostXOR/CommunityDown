import json

# Currently broken for most types of posts
def parsePost(post):
    # Get the data we really want
    post = post["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]
    output = {}

    output["postID"] = post["postId"]
    output["authorDisplayName"] = post["authorText"]["runs"][0]["text"]
    output["authorImage"] = "https:" + post["authorThumbnail"]["thumbnails"][-1]["url"]
    output["authorID"] = post["authorEndpoint"]["browseEndpoint"]["browseId"]
    output["contentText"] = post["contentText"]["runs"][0]["text"]
    output["timeText"] = post["publishedTimeText"]["runs"][0]["text"]
    output["likeText"] = post["voteCount"]["simpleText"]
    likeCountText = post["actionButtons"]["commentActionButtonsRenderer"]["likeButton"]["toggleButtonRenderer"]["accessibilityData"]["accessibilityData"]["label"]
    output["likeCount"] = int("".join([c for c in likeCountText if c.isdigit()]))
    output["commentText"] = post["actionButtons"]["commentActionButtonsRenderer"]["replyButton"]["buttonRenderer"]["text"]["simpleText"]
    return output