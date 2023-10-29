import unittest
from channel import Channel

# Various formats of channel name/ID to test channel resolving
valid_channel_strings = [
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
invalid_channel_strings = [
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

# Posts of the test channel for testing Post (and by extension fetch_posts and parse_post)
testPosts = channelNormal.fetch_posts()

# Comments of some test posts for testing Comment (and by extension fetch_comments and parse_comment)
noComments = testPosts[0].fetch_comments()
oneComment = testPosts[11].fetch_comments()
topComments = testPosts[12].fetch_comments()
chronoComments = testPosts[12].fetch_comments(chronological = True)

class TestChannel(unittest.TestCase):
    """Unit test the Channel class."""

    def test_exists(self):
        """Test Channel.exists() correctly determines if a channel exists."""
        for channel_string in valid_channel_strings:
            channel = Channel(channel_string)
            self.assertTrue(channel.exists())

        for channel_string in invalid_channel_strings:
            channel = Channel(channel_string)
            self.assertFalse(channel.exists())

    def test_has_community(self):
        """Test Channel.has_community correctly determines if a channel has a Community page."""
        self.assertTrue(channelNormal.has_community())
        self.assertTrue(channelEmpty.has_community())
        self.assertFalse(channelNoCommunity.has_community())
        self.assertFalse(channelInvalid.has_community())

    def test_channel_id(self):
        """Test Channel.channel_id returns a channel's correct ID (or None if invalid)."""
        self.assertEqual(channelNormal.channel_id(), "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(channelEmpty.channel_id(), "UCv952x-cd5Dg3ZBd9GtMVSw")
        self.assertEqual(channelNoCommunity.channel_id(), "UCfRiDC9KN7TD3JFKKUG5Plg")
        self.assertEqual(channelInvalid.channel_id(), None)

    def test_fetch_posts(self):
        """Test Channel.fetch_posts returns the correct amount of posts."""
        self.assertEqual(len(channelNormal.fetch_posts()), 17)
        self.assertEqual(channelEmpty.fetch_posts(), [])
        self.assertEqual(channelNoCommunity.fetch_posts(), None)
        self.assertEqual(channelInvalid.fetch_posts(), None)

    def test_fetch_posts_limit(self):
        """Test Channel.fetch_posts limit function returns correct amount of posts and the right posts."""
        limit0 = channelNormal.fetch_posts(limit = 0)
        limit7 = channelNormal.fetch_posts(limit = 7)
        limit13 = channelNormal.fetch_posts(limit = 13)
        self.assertEqual(limit0, [])
        self.assertEqual(len(limit7), 7)
        self.assertEqual(len(limit13), 13)
        self.assertEqual([o.postID for o in limit7], [o.postID for o in limit13[-7:]])

class TestPost(unittest.TestCase):
    """Unit test the Post class."""

    def test_text_post(self):
        """Test that text-only posts are parsed correctly."""
        post = testPosts[0]
        self.assertEqual(post.postID, "UgkxN3xglfBx_R4q55qU_Z1Hzey5Ah9CyTpE")
        self.assertEqual(post.authorID, "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(post.authorDisplayName, "CommunityDown Test Channel")
        self.assertEqual(post.authorImageURL, "https://yt3.googleusercontent.com/ytc/APkrFKZYhSYg1uorjLPobZEDG0QOajyyEyKkDmprqcLsLalZTKmtVx_xBxZe7faUD1B4=s76-c-k-c0x00ffffff-no-rj-mo")
        self.assertTrue(post.likeCount >= 0)
        self.assertEqual(post.comment_countText, "0")
        self.assertFalse(post.edited)
        self.assertTrue(post.timeText.endswith("ago"))
        self.assertEqual(post.contentText, "Test Post Text Only")
        self.assertEqual(post.attachment, None)


    def test_multi_line_text_post(self):
        """Test that multi-line posts are parsed correctly."""
        post = testPosts[15]
        self.assertEqual(post.postID, "UgkxVWzwSGoR5O_JCxWGeBbIQALIb1grfk4u")
        self.assertEqual(post.contentText, "Test Post Many New\n\nLines\n\n\nSo Many\nNew\n\n\nLines\n\n\nbackslash n go brr\n\n\n\nowo\nuwu\nowo\nuwu")

    def test_link_text_post(self):
        """Test that posts with links are parsed correctly."""
        post = testPosts[16]
        self.assertEqual(post.postID, "Ugkx9HySrooC8q8OlaGQnt3tuA1TeGaILbkC")
        self.assertEqual(post.contentText, "Test Post With Link: https://example.com")

    def test_text_image_post(self):
        """Test that posts with images are parsed correctly."""
        post = testPosts[1]
        self.assertEqual(post.postID, "UgkxDE7a1eW5RZGvEm4jXldpMxHDuM6UpruZ")
        self.assertEqual(post.contentText, "Test Post Text With Image")
        self.assertEqual(post.attachment["type"], "image")
        self.assertEqual(post.attachment["url"], "https://yt3.ggpht.com/LD3QXmo4_3ix3b2axlqfJeUQ1YvOZdeLCkIY646w9xCOj-IR3V2u00xrWTyOEzcv1Z0gBTND0hT8=s512-c-fcrop64=1,00000000ffffffff-nd-v1")

    def test_text_multi_image_post(self):
        """Test that posts with multiple images are parsed correctly."""
        post = testPosts[2]
        self.assertEqual(post.postID, "UgkxDE0-ktPPh_QNsqC9ZLZgzpbaazujegHF")
        self.assertEqual(post.contentText, "Test Post Text With Multiple Images")
        self.assertEqual(post.attachment["type"], "multiImage")
        self.assertEqual(post.attachment["urls"][0], "https://yt3.ggpht.com/G5KKGBwa36uhKNKZ3LqzsUJZ7Gi19Msp1E_1lEMk_HC6aY1_5dQoXSIi8HXohuwdsh2PufCnrgl6uQ=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertTrue(len(post.attachment["urls"]) == 5)

    def test_image_post(self):
        """Test that posts with only an image are parsed correctly."""
        post = testPosts[3]
        self.assertEqual(post.postID, "UgkxE0R5C37qvZ8PC1rcg9WgJiz-XERxgw4V")
        self.assertEqual(post.contentText, None)
        self.assertEqual(post.attachment["type"], "image")
        self.assertEqual(post.attachment["url"], "https://yt3.ggpht.com/w3pdzdEXiiqa4UEdxcon2Jwt1nNHF6eM4Yu8KcvU21_vIkOTS8kGKJJQfwnu4Wy3EUpdGABFo4cR=s512-c-fcrop64=1,00000000ffffffff-nd-v1")

    def test_multi_image_post(self):
        """Test that posts with only multiple images are parsed correctly."""
        post = testPosts[4]
        self.assertEqual(post.postID, "UgkxY2O9N8cX9rMNMK50lOK6VXMvw05uyTCa")
        self.assertEqual(post.contentText, None)
        self.assertEqual(post.attachment["type"], "multiImage")
        self.assertEqual(post.attachment["urls"][0], "https://yt3.ggpht.com/ucbXFS7xEjYaU3qke1Xo7wAx8X6BOJWAidq-zhLO9EjXv19e0lORwFlIbbn3dApzTAlCTtu5kG8pvA=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertEqual(len(post.attachment["urls"]), 5)

    def test_edited_post(self):
        """Test that edited posts have the edited attribute."""
        post = testPosts[5]
        self.assertEqual(post.postID, "Ugkxh2DuCHmAmyjdAKVv_dcmrvMj787b2OL1")
        self.assertEqual(post.contentText, "Test Post Edit")
        self.assertTrue(post.edited)
        self.assertTrue(post.timeText.endswith("ago"))

    def test_poll(self):
        """Test that posts with polls are parsed correctly."""
        post = testPosts[6]
        self.assertEqual(post.postID, "UgkxQ2GoSAnhj3KbrWyvGVLLI16-oEcLJV2k")
        self.assertEqual(post.contentText, "Test Post Text Poll")
        self.assertEqual(post.attachment["type"], "poll")
        self.assertTrue(post.attachment["votesText"].endswith("votes"))
        self.assertEqual(post.attachment["choices"], ["Choice One", "Choice Two", "Choice Three", "Choice Four"])
        self.assertEqual(post.attachment["imageURLs"], None)

    def test_image_poll(self):
        """Test that posts with image polls are parsed correctly."""
        post = testPosts[9]
        self.assertEqual(post.postID, "UgkxWDZnrAVYI8w0jQOpRyC7XrJa9Ey_k1Wg")
        self.assertEqual(post.contentText, "Image Poll")
        self.assertEqual(post.attachment["type"], "poll")
        self.assertTrue(post.attachment["votesText"].endswith("votes"))
        self.assertEqual(post.attachment["choices"], ["uwu", "owo"])
        self.assertEqual(post.attachment["imageURLs"][0], "https://yt3.ggpht.com/mMRTwi6OYV7aSWl9o7Y44S87fUZiImACxeVncwLa2Pvl9DDiDyzM8aqNrVyftFcSqoF8_sP6PB5h=s512-c-fcrop64=1,00000000ffffffff-nd-v1")
        self.assertEqual(len(post.attachment["imageURLs"]), 2)

    def test_video_embed(self):
        """Test that posts with embedded videos are parsed correctly."""
        # TODO: This should be changed to a video on the test channel at some point
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

    def test_quiz(self):
        """Test that posts with quizzes are parsed correctly."""
        post = testPosts[7]
        self.assertEqual(post.postID, "Ugkxj5sWVNGmEZE73g2zxSea8k89GlceOA1d")
        self.assertEqual(post.contentText, "Test Post Quiz")
        self.assertEqual(post.attachment["type"], "quiz")
        self.assertEqual(post.attachment["choices"], ["Answer 1", "Answer 2", "Answer 3 (Correct)"])
        self.assertEqual(post.attachment["correctChoice"], 2)
        self.assertEqual(post.attachment["explanation"], "Explanation For Correct Answer")
        self.assertTrue(post.attachment["answerCountText"].endswith("answered"))

    def test_comment_count(self):
        """Test that the comment count of posts is correct."""
        post = testPosts[12]
        self.assertEqual(post.postID, "UgkximjhpHrqqxHue2IDIpiDRDVK9Q3J8z4c")
        self.assertEqual(post.contentText, "Test Post With Many Comments")
        self.assertEqual(post.comment_countText, "43")
        self.assertEqual(post.comment_count, 43)
        post.fetch_comments(limit = 0)

    def test_vote_count(self):
        """Test that the vote count of posts is correct(ish)."""
        post = testPosts[13]
        self.assertEqual(post.postID, "UgkxXrf-6FdrjY1oY5Og-2V8cm_Hmx1Zb8IS")
        self.assertEqual(post.contentText, "Test Post With Vote")
        self.assertTrue(post.likeCount >= 1)

class TestComment(unittest.TestCase):
    """Test the Comment class (and by extension the parse_comment function)."""


    def test_no_comments(self):
        """Test that a post with no comments returns an empty array."""
        self.assertEqual(noComments, [])

    def test_one_comment(self):
        """Test that a post with one comment is parsed correctly."""
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

    def test_comments(self):
        """Test comments from a post with multiple comments are fetched and parsed correctly."""
        # All the comments was fetched from the post
        self.assertEqual(len(topComments), 35)
        self.assertEqual(len(chronoComments), 35)
        # Comment content and reply count is correct (for the first two comments at least)
        self.assertEqual(chronoComments[0].commentID, "UgxmOxIaaaHFkH22tj94AaABAg")
        self.assertEqual(chronoComments[0].contentText, "Hello")
        self.assertEqual(chronoComments[0].replyCount, 3)
        self.assertEqual(chronoComments[1].commentID, "UgzbF4D7-o3C9P2izEV4AaABAg")
        self.assertEqual(chronoComments[1].contentText, "Test Test")

    def test_edited_comment(self):
        """Test an edited comment has the edited attribute."""
        self.assertEqual(chronoComments[33].commentID, "UgwWsiDrEvru2rp9M8Z4AaABAg")
        self.assertEqual(chronoComments[33].contentText, "youtube api = stupid and i hate (edited nvm I love youtube api (jk))")
        self.assertEqual(chronoComments[33].replyCount, 4)
        self.assertTrue(chronoComments[33].edited)

    def test_complex_comment(self):
        """Test a complex comment (with emojis, links, and formatting) is parsed correctly."""
        self.assertEqual(chronoComments[34].commentID, "Ugw6VVsZhhzklrzJdMV4AaABAg")
        self.assertEqual(chronoComments[34].contentText,
    # Explicit 0x20 because trailing space gets removed by editors
"""Comment Text Parsing
Emojis::face-blue-smiling: also :text-green-game-over:\x20

Bold: *bold*
Italic: _italic_
Strikethrough: -strikethrough-
All: -_*bold italic strikethrough*_-

Link: https://example.com

More newlines


uwu""")

    def test_fetch_comments_imit(self):
        """Test Post.fetch_comments limit function returns correct amount of comments and the right comments."""
        limit0 = testPosts[12].fetch_comments(limit = 0)
        limit17 = testPosts[12].fetch_comments(limit = 17)
        limit32 = testPosts[12].fetch_comments(limit = 32)
        self.assertEqual(limit0, [])
        self.assertEqual(len(limit17), 17)
        self.assertEqual(len(limit32), 32)
        self.assertEqual([o.commentID for o in limit17], [o.commentID for o in limit32[-17:]])

unittest.main()