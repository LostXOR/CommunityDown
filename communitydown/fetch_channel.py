import requests
import re
import communitydown

"""fetch_channel"""
def fetch_channel(channel):
    """Fetch a channel's information given its ID."""

    # Attempt to get channel page
    if channel.startswith("@"):
        response = requests.get("https://youtube.com/" + channel, timeout = 5)
    elif channel.startswith("https://"):
        response = requests.get(channel, timeout = 5)
    elif "youtube.com" in channel:
        response = requests.get("https://" + channel, timeout = 5)
    else:
        response = requests.get("https://youtube.com/channel/" + channel, timeout = 5)

    matches = re.findall(r'(?<=content="https:\/\/www\.youtube\.com\/channel\/).*?(?="|\?)', response.text)

    if len(matches) == 0:
        return None
    else:
        return communitydown.Channel({
            "channelID": matches[0],
            "hasCommunityTab": '"title":"Community"' in response.text
        })
