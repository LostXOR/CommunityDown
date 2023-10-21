import requests, re

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
        pass