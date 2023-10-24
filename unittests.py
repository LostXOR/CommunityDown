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
# Grab posts of a channel for testing parsePost
testPosts = channelNormal.fetchPosts()

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
        self.assertTrue(len(channelNormal.fetchPosts()) == 15)
        self.assertEqual(channelEmpty.fetchPosts(), [])
        self.assertEqual(channelNoCommunity.fetchPosts(), None)
        self.assertEqual(channelInvalid.fetchPosts(), None)

class parsePost(unittest.TestCase):

    def testTextPost(self):
        post = communitydown.parsePost(testPosts[0])
        self.assertEqual(post["postID"], "UgkxN3xglfBx_R4q55qU_Z1Hzey5Ah9CyTpE")
        self.assertEqual(post["authorID"], "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(post["authorDisplayName"], "CommunityDown Test Channel")
        self.assertEqual(post["authorImageURL"], "https://yt3.googleusercontent.com/ytc/APkrFKZYhSYg1uorjLPobZEDG0QOajyyEyKkDmprqcLsLalZTKmtVx_xBxZe7faUD1B4=s76-c-k-c0x00ffffff-no-rj-mo")
        self.assertTrue(post["likeCount"] >= 0)
        self.assertTrue(int(post["likeCountText"]) >= 0)
        self.assertEqual(post["commentCountText"], "0")
        self.assertTrue(post["timeText"].endswith("ago"))
        self.assertEqual(post["contentText"], "Test Post Text Only")
        self.assertEqual(post["attachment"], None)

    def testTextImagePost(self):
        post = communitydown.parsePost(testPosts[1])
        self.assertEqual(post["contentText"], "Test Post Text With Image")
        self.assertEqual(post["attachment"]["type"], "image")
        self.assertEqual(post["attachment"]["url"], "https://yt3.ggpht.com/LD3QXmo4_3ix3b2axlqfJeUQ1YvOZdeLCkIY646w9xCOj-IR3V2u00xrWTyOEzcv1Z0gBTND0hT8=s512-c-fcrop64=1,00000000ffffffff-nd-v1")

    def testTextMultiImagePost(self):
        post = communitydown.parsePost(testPosts[2])
        self.assertEqual(post["postID"], "UgkxDE0-ktPPh_QNsqC9ZLZgzpbaazujegHF")
        self.assertEqual(post["contentText"], "Test Post Text With Multiple Images")
        self.assertEqual(post["attachment"]["type"], "multiImage")
        self.assertEqual(post["attachment"]["urls"][0], "https://yt3.ggpht.com/G5KKGBwa36uhKNKZ3LqzsUJZ7Gi19Msp1E_1lEMk_HC6aY1_5dQoXSIi8HXohuwdsh2PufCnrgl6uQ=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertTrue(len(post["attachment"]["urls"]) == 5)

    def testImagePost(self):
        post = communitydown.parsePost(testPosts[3])
        self.assertEqual(post["postID"], "UgkxE0R5C37qvZ8PC1rcg9WgJiz-XERxgw4V")
        self.assertEqual(post["contentText"], None)
        self.assertEqual(post["attachment"]["type"], "image")
        self.assertEqual(post["attachment"]["url"], "https://yt3.ggpht.com/w3pdzdEXiiqa4UEdxcon2Jwt1nNHF6eM4Yu8KcvU21_vIkOTS8kGKJJQfwnu4Wy3EUpdGABFo4cR=s512-c-fcrop64=1,00000000ffffffff-nd-v1")

    def testMultiImagePost(self):
        post = communitydown.parsePost(testPosts[4])
        self.assertEqual(post["postID"], "UgkxY2O9N8cX9rMNMK50lOK6VXMvw05uyTCa")
        self.assertEqual(post["contentText"], None)
        self.assertEqual(post["attachment"]["type"], "multiImage")
        self.assertEqual(post["attachment"]["urls"][0], "https://yt3.ggpht.com/ucbXFS7xEjYaU3qke1Xo7wAx8X6BOJWAidq-zhLO9EjXv19e0lORwFlIbbn3dApzTAlCTtu5kG8pvA=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertTrue(len(post["attachment"]["urls"]) == 5)

    def testPoll(self):
        post = communitydown.parsePost(testPosts[6])
        self.assertEqual(post["postID"], "UgkxQ2GoSAnhj3KbrWyvGVLLI16-oEcLJV2k")
        self.assertEqual(post["contentText"], "Test Post Text Poll")
        self.assertEqual(post["attachment"]["type"], "poll")
        self.assertTrue(post["attachment"]["votesText"].endswith("vote"))
        self.assertEqual(post["attachment"]["choices"], ["Choice One", "Choice Two", "Choice Three", "Choice Four"])
        self.assertEqual(post["attachment"]["imageURLs"], None)

    def testImagePoll(self):
        post = communitydown.parsePost(testPosts[9])
        # TODO: Add tests for image poll

    def testVideoEmbed(self):
        post = communitydown.parsePost(testPosts[8])
        self.assertEqual(post["postID"], "Ugkx0mOGgVuFfy8znxJWfIdryu6XL2iQHdOu")
        self.assertEqual(post["contentText"], "Video Post")
        self.assertEqual(post["attachment"]["type"], "video")
        # TODO: Add asserts for video properties
    def testQuiz(self):
        post = communitydown.parsePost(testPosts[7])
        self.assertEqual(post["postID"], "Ugkxj5sWVNGmEZE73g2zxSea8k89GlceOA1d")
        self.assertEqual(post["contentText"], "Test Post Quiz")
        self.assertEqual(post["attachment"]["type"], "quiz")
        self.assertEqual(post["attachment"]["choices"], ["Answer 1", "Answer 2", "Answer 3 (Correct)"])
        self.assertEqual(post["attachment"]["correctChoice"], 2)
        self.assertEqual(post["attachment"]["explanation"], "Explanation For Correct Answer")
        self.assertTrue(post["attachment"]["answerCountText"].endswith("answered"))

    def testCommentCount(self):
        post = communitydown.parsePost(testPosts[12])
        # TODO: Add tests for comment count

    def testVoteCount(self):
        post = communitydown.parsePost(testPosts[13])
        # TODO: Add tests for vote count

unittest.main()
