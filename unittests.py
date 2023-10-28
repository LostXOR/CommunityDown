import unittest
from channel import Channel

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
channelNormal = Channel("@CommunityDownTestChannel")
channelEmpty = Channel("@CommunityDownTestEmpty")
channelNoCommunity = Channel("@CommunityDownTestNoCommunity")
channelInvalid = Channel("@invalid channel")
# Grab posts of a channel for testing parsePost (and by extension fetchPosts)
testPosts = channelNormal.fetchPosts()
# Grab comments of a channel for testing parseComment (and by extension fetchComment)
noComments = testPosts[0].fetchComments()
oneComment = testPosts[11].fetchComments()
topComments = testPosts[12].fetchComments()
chronoComments = testPosts[12].fetchComments(chronological = True)

class TestChannel(unittest.TestCase):

    def testExists(self):
        for channelString in validChannelStrings:
            channel = Channel(channelString)
            self.assertTrue(channel.exists())

        for channelString in invalidChannelStrings:
            channel = Channel(channelString)
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
        self.assertEqual(len(channelNormal.fetchPosts()), 16)
        self.assertEqual(channelEmpty.fetchPosts(), [])
        self.assertEqual(channelNoCommunity.fetchPosts(), None)
        self.assertEqual(channelInvalid.fetchPosts(), None)

class parsePost(unittest.TestCase):

    def testTextPost(self):
        post = testPosts[0]
        self.assertEqual(post.postID, "UgkxN3xglfBx_R4q55qU_Z1Hzey5Ah9CyTpE")
        self.assertEqual(post.authorID, "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(post.authorDisplayName, "CommunityDown Test Channel")
        self.assertEqual(post.authorImageURL, "https://yt3.googleusercontent.com/ytc/APkrFKZYhSYg1uorjLPobZEDG0QOajyyEyKkDmprqcLsLalZTKmtVx_xBxZe7faUD1B4=s76-c-k-c0x00ffffff-no-rj-mo")
        self.assertTrue(post.likeCount >= 0)
        self.assertEqual(post.commentCountText, "0")
        self.assertFalse(post.edited)
        self.assertTrue(post.timeText.endswith("ago"))
        self.assertEqual(post.contentText, "Test Post Text Only")
        self.assertEqual(post.attachment, None)

    def testTextImagePost(self):
        post = testPosts[1]
        self.assertEqual(post.contentText, "Test Post Text With Image")
        self.assertEqual(post.attachment["type"], "image")
        self.assertEqual(post.attachment["url"], "https://yt3.ggpht.com/LD3QXmo4_3ix3b2axlqfJeUQ1YvOZdeLCkIY646w9xCOj-IR3V2u00xrWTyOEzcv1Z0gBTND0hT8=s512-c-fcrop64=1,00000000ffffffff-nd-v1")

    def testTextMultiImagePost(self):
        post = testPosts[2]
        self.assertEqual(post.postID, "UgkxDE0-ktPPh_QNsqC9ZLZgzpbaazujegHF")
        self.assertEqual(post.contentText, "Test Post Text With Multiple Images")
        self.assertEqual(post.attachment["type"], "multiImage")
        self.assertEqual(post.attachment["urls"][0], "https://yt3.ggpht.com/G5KKGBwa36uhKNKZ3LqzsUJZ7Gi19Msp1E_1lEMk_HC6aY1_5dQoXSIi8HXohuwdsh2PufCnrgl6uQ=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertTrue(len(post.attachment["urls"]) == 5)

    def testImagePost(self):
        post = testPosts[3]
        self.assertEqual(post.postID, "UgkxE0R5C37qvZ8PC1rcg9WgJiz-XERxgw4V")
        self.assertEqual(post.contentText, None)
        self.assertEqual(post.attachment["type"], "image")
        self.assertEqual(post.attachment["url"], "https://yt3.ggpht.com/w3pdzdEXiiqa4UEdxcon2Jwt1nNHF6eM4Yu8KcvU21_vIkOTS8kGKJJQfwnu4Wy3EUpdGABFo4cR=s512-c-fcrop64=1,00000000ffffffff-nd-v1")

    def testMultiImagePost(self):
        post = testPosts[4]
        self.assertEqual(post.postID, "UgkxY2O9N8cX9rMNMK50lOK6VXMvw05uyTCa")
        self.assertEqual(post.contentText, None)
        self.assertEqual(post.attachment["type"], "multiImage")
        self.assertEqual(post.attachment["urls"][0], "https://yt3.ggpht.com/ucbXFS7xEjYaU3qke1Xo7wAx8X6BOJWAidq-zhLO9EjXv19e0lORwFlIbbn3dApzTAlCTtu5kG8pvA=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertEqual(len(post.attachment["urls"]), 5)

    def testEditedPost(self):
        post = testPosts[5]
        self.assertEqual(post.postID, "Ugkxh2DuCHmAmyjdAKVv_dcmrvMj787b2OL1")
        self.assertEqual(post.contentText, "Test Post Edit")
        self.assertTrue(post.edited)
        self.assertTrue(post.timeText.endswith("ago"))

    def testPoll(self):
        post = testPosts[6]
        self.assertEqual(post.postID, "UgkxQ2GoSAnhj3KbrWyvGVLLI16-oEcLJV2k")
        self.assertEqual(post.contentText, "Test Post Text Poll")
        self.assertEqual(post.attachment["type"], "poll")
        self.assertTrue(post.attachment["votesText"].endswith("votes"))
        self.assertEqual(post.attachment["choices"], ["Choice One", "Choice Two", "Choice Three", "Choice Four"])
        self.assertEqual(post.attachment["imageURLs"], None)

    def testImagePoll(self):
        post = testPosts[9]
        self.assertEqual(post.postID, "UgkxWDZnrAVYI8w0jQOpRyC7XrJa9Ey_k1Wg")
        self.assertEqual(post.contentText, "Image Poll")
        self.assertEqual(post.attachment["type"], "poll")
        self.assertTrue(post.attachment["votesText"].endswith("votes"))
        self.assertEqual(post.attachment["choices"], ["uwu", "owo"])
        self.assertEqual(post.attachment["imageURLs"][0], "https://yt3.ggpht.com/mMRTwi6OYV7aSWl9o7Y44S87fUZiImACxeVncwLa2Pvl9DDiDyzM8aqNrVyftFcSqoF8_sP6PB5h=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertEqual(len(post.attachment["imageURLs"]), 2)

    # This should be changed to a video on the test channel at some point
    def testVideoEmbed(self):
        post = testPosts[8]
        self.assertEqual(post.postID, "Ugkx0mOGgVuFfy8znxJWfIdryu6XL2iQHdOu")
        self.assertEqual(post.contentText, "Video Post")
        self.assertEqual(post.attachment["type"], "video")
        self.assertEqual(post.attachment["ID"], "dQw4w9WgXcQ")
        self.assertEqual(post.attachment["thumbnailURL"], "https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDX3LgTmArIBIk6uvvz4y5p95MOcg")
        self.assertEqual(post.attachment["title"], "Rick Astley - Never Gonna Give You Up (Official Music Video)")
        self.assertTrue(post.attachment["descriptionSnippet"].startswith("The official video"))
        self.assertEqual(post.attachment["authorDisplayName"], "Rick Astley")
        self.assertTrue(post.attachment["timeText"].endswith("years ago"))
        self.assertEqual(post.attachment["lengthText"], "3:33")
        self.assertTrue(post.attachment["viewCount"] >= 1462235415) # View count as of writing this test
        self.assertTrue(post.attachment["viewCountText"].endswith("views"))

    def testQuiz(self):
        post = testPosts[7]
        self.assertEqual(post.postID, "Ugkxj5sWVNGmEZE73g2zxSea8k89GlceOA1d")
        self.assertEqual(post.contentText, "Test Post Quiz")
        self.assertEqual(post.attachment["type"], "quiz")
        self.assertEqual(post.attachment["choices"], ["Answer 1", "Answer 2", "Answer 3 (Correct)"])
        self.assertEqual(post.attachment["correctChoice"], 2)
        self.assertEqual(post.attachment["explanation"], "Explanation For Correct Answer")
        self.assertTrue(post.attachment["answerCountText"].endswith("answered"))

    def testCommentCount(self):
        post = testPosts[12]
        self.assertEqual(post.postID, "UgkximjhpHrqqxHue2IDIpiDRDVK9Q3J8z4c")
        self.assertEqual(post.contentText, "Test Post With Many Comments")
        self.assertEqual(post.commentCountText, "43")

    def testVoteCount(self):
        post = testPosts[13]
        self.assertEqual(post.postID, "UgkxXrf-6FdrjY1oY5Og-2V8cm_Hmx1Zb8IS")
        self.assertEqual(post.contentText, "Test Post With Vote")
        self.assertTrue(post.likeCount >= 1)

class parseComment(unittest.TestCase):

    def testNoComments(self):
        self.assertEqual(noComments, [])

    def testOneComment(self):
        self.assertTrue(len(oneComment), 1)
        self.assertEqual(oneComment[0].authorID, "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(oneComment[0].authorDisplayName, "@CommunityDownTest")
        self.assertEqual(oneComment[0].authorImageURL, "https://yt3.ggpht.com/ytc/APkrFKZYhSYg1uorjLPobZEDG0QOajyyEyKkDmprqcLsLalZTKmtVx_xBxZe7faUD1B4=s176-c-k-c0x00ffffff-no-rj")
        self.assertEqual(oneComment[0].commentID, "UgycOEolpmxD37kcJJN4AaABAg")
        self.assertTrue(oneComment[0].likeCount >= 1)
        self.assertEqual(oneComment[0].replyCount, 0)
        self.assertTrue(oneComment[0].timeText.endswith("ago"))
        self.assertFalse(oneComment[0].edited)
        self.assertEqual(oneComment[0].contentText, "Hurdle Durdle")

    def testManyComments(self):
        self.assertEqual(len(topComments), 35)
        self.assertEqual(len(chronoComments), 35)
        self.assertEqual(chronoComments[0].commentID, "UgxmOxIaaaHFkH22tj94AaABAg")
        self.assertEqual(chronoComments[0].contentText, "Hello")
        self.assertEqual(chronoComments[0].replyCount, 3)

        self.assertEqual(chronoComments[1].commentID, "UgzbF4D7-o3C9P2izEV4AaABAg")
        self.assertEqual(chronoComments[1].contentText, "Test Test")

        self.assertEqual(chronoComments[33].commentID, "UgwWsiDrEvru2rp9M8Z4AaABAg")
        self.assertEqual(chronoComments[33].contentText, "youtube api = stupid and i hate (edited nvm I love youtube api (jk))")
        self.assertEqual(chronoComments[33].replyCount, 4)
        self.assertTrue(chronoComments[33].edited)

unittest.main()
