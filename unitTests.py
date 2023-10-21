import unittest
import communitydown

# Various formats of channel name/ID to test channel resolving
validChannelStrings = [
    "@CommunityDownTestChannel",
    "UCSHozX8N-F7GygP9PIIYxLw",
    "https://youtube.com/@CommunityDownTestChannel",
    "youtube.com/channel/UCSHozX8N-F7GygP9PIIYxLw",
    "@CommunityDownTestEmpty",
    "UCv952x-cd5Dg3ZBd9GtMVSw",
    "https://youtube.com/@CommunityDownTestEmpty",
    "youtube.com/channel/UCv952x-cd5Dg3ZBd9GtMVSw",
    "@CommunityDownTestNoCommunity",
    "UCfRiDC9KN7TD3JFKKUG5Plg",
    "https://youtube.com/@CommunityDownTestNoCommunity",
    "youtube.com/channel/UCfRiDC9KN7TD3JFKKUG5Plg"
]
invalidChannelStrings = [
    "@invalid channel",
    "UCSHoxB12-34567P9PIIYxLw",
    "https://youtube.com/invalidchannelinvalidchannelinvalidchannel",
    "youtube.com/channel/UCSHoxB12-34567P9PIIYxLw"
]
# Test channels with community posts, an empty community tab, no community tab, and invalid
channelNormal = communitydown.Channel("@CommunityDownTestChannel")
channelEmpty = communitydown.Channel("@CommunityDownTestEmpty")
channelNoCommunity = communitydown.Channel("@CommunityDownTestNoCommunity")
channelInvalid = communitydown.Channel("@invalid channel")

class TestChannel(unittest.TestCase):

    def testExists(self):
        for channelString in validChannelStrings:
            channel = communitydown.Channel(channelString)
            self.assertTrue(channel.exists())

        for channelString in invalidChannelStrings:
            channel = communitydown.Channel(channelString)
            self.assertFalse(channel.exists())

    def testHasCommunity(self):
        self.assertTrue(channelNormal.hasCommunity())
        self.assertTrue(channelEmpty.hasCommunity())
        self.assertFalse(channelNoCommunity.hasCommunity())
        self.assertFalse(channelInvalid.hasCommunity())

    def testChannelID(self):
        self.assertEqual(channelNormal.channelID(), "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(channelEmpty.channelID(), "UCv952x-cd5Dg3ZBd9GtMVSw")
        self.assertEqual(channelNoCommunity.channelID(), "UCfRiDC9KN7TD3JFKKUG5Plg"),
        self.assertEqual(channelInvalid.channelID(), None)

    def testFetchPosts(self):
        self.assertTrue(len(channelNormal.fetchPosts() >= 13))
        self.assertEqual(channelEmpty.fetchPosts(), [])
        self.assertEqual(channelNoCommunity.fetchPosts(), None)
        self.assertEqual(channelInvalid.fetchPosts(), None)

unittest.main()