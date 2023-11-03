"""Unit tests! (most useful docstring)"""

import unittest
import communitydown

# Test channels
normal_channel = communitydown.fetch_channel("UCSHozX8N-F7GygP9PIIYxLw")
empty_channel = communitydown.fetch_channel("UCv952x-cd5Dg3ZBd9GtMVSw")
no_community_channel = communitydown.fetch_channel("UCfRiDC9KN7TD3JFKKUG5Plg")
invalid_channel = communitydown.fetch_channel("UCfRiDC9KN7TD3JFKKUG5Qmh")

# Test posts
test_posts = normal_channel.fetch_posts()

# Test comments
no_comments = test_posts[0].fetch_comments()
one_comment = test_posts[11].fetch_comments()
top_comments = test_posts[12].fetch_comments()
chrono_comments = test_posts[12].fetch_comments(chronological = True)

class TestFetchChannel(unittest.TestCase):

    def test_channel_finding(self):
        # Various formats of channel name/ID to test channel finding
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
        for channel_string in valid_channel_strings:
            self.assertFalse(communitydown.fetch_channel(channel_string) is None)

        for channel_string in invalid_channel_strings:
            self.assertTrue(communitydown.fetch_channel(channel_string) is None)

    def test_channel_data(self):
        self.assertFalse(normal_channel is None)
        self.assertFalse(empty_channel is None)
        self.assertFalse(no_community_channel is None)
        self.assertTrue(invalid_channel is None)
        self.assertTrue(normal_channel.has_community_tab())
        self.assertTrue(empty_channel.has_community_tab())
        self.assertFalse(no_community_channel.has_community_tab())

#class TestFetchPost(unittest.TestCase):
#    pass

#class testFetchComment(unittest.TestCase):
#    pass

class TestChannel(unittest.TestCase):

    def test_normal_channel(self):
        self.assertEqual(normal_channel.channel_id(), "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertTrue(normal_channel.has_community_tab())

    def test_empty_channel(self):
        self.assertEqual(empty_channel.channel_id(), "UCv952x-cd5Dg3ZBd9GtMVSw")
        self.assertTrue(empty_channel.has_community_tab())

    def test_no_community_channel(self):
        self.assertEqual(no_community_channel.channel_id(), "UCfRiDC9KN7TD3JFKKUG5Plg")
        self.assertFalse(no_community_channel.has_community_tab())


class TestPost(unittest.TestCase):

    def test_text_post(self):
        """Test that text-only posts are parsed correctly."""
        data = test_posts[0].data()
        self.assertEqual(data["postID"], "UgkxN3xglfBx_R4q55qU_Z1Hzey5Ah9CyTpE")
        self.assertEqual(data["authorID"], "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(data["authorDisplayName"], "CommunityDown Test Channel")
        self.assertTrue(data["authorImageURL"].startswith("https://yt3.googleusercontent.com"))
        self.assertTrue(data["likeCount"] >= 0)
        self.assertEqual(data["commentCountText"], "0")
        self.assertFalse(data["edited"])
        self.assertTrue(data["timeText"].endswith("ago"))
        self.assertEqual(data["contentText"], "Test Post Text Only")
        self.assertEqual(data["attachment"], None)


    def test_multi_line_text_post(self):
        """Test that multi-line posts are parsed correctly."""
        data = test_posts[15].data()
        self.assertEqual(data["postID"], "UgkxVWzwSGoR5O_JCxWGeBbIQALIb1grfk4u")
        self.assertEqual(data["contentText"],
"""Test Post Many New

Lines


So Many
New


Lines


backslash n go brr



owo
uwu
owo
uwu""")

    def test_link_text_post(self):
        """Test that posts with links are parsed correctly."""
        data = test_posts[16].data()
        self.assertEqual(data["postID"], "Ugkx9HySrooC8q8OlaGQnt3tuA1TeGaILbkC")
        self.assertEqual(data["contentText"], "Test Post With Link: https://example.com")

    def test_text_image_post(self):
        """Test that posts with images are parsed correctly."""
        data = test_posts[1].data()
        self.assertEqual(data["postID"], "UgkxDE7a1eW5RZGvEm4jXldpMxHDuM6UpruZ")
        self.assertEqual(data["contentText"], "Test Post Text With Image")
        self.assertEqual(data["attachment"]["type"], "image")
        self.assertTrue(data["attachment"]["URL"].startswith("https://yt3.ggpht.com"))

    def test_text_multi_image_post(self):
        """Test that posts with multiple images are parsed correctly."""
        data = test_posts[2].data()
        self.assertEqual(data["postID"], "UgkxDE0-ktPPh_QNsqC9ZLZgzpbaazujegHF")
        self.assertEqual(data["contentText"], "Test Post Text With Multiple Images")
        self.assertEqual(data["attachment"]["type"], "multiImage")
        self.assertTrue(data["attachment"]["URLs"][0].startswith("https://yt3.ggpht.com"))
        self.assertTrue(len(data["attachment"]["URLs"]) == 5)

    def test_image_post(self):
        """Test that posts with only an image are parsed correctly."""
        data = test_posts[3].data()
        self.assertEqual(data["postID"], "UgkxE0R5C37qvZ8PC1rcg9WgJiz-XERxgw4V")
        self.assertEqual(data["contentText"], None)
        self.assertEqual(data["attachment"]["type"], "image")
        self.assertTrue(data["attachment"]["URL"].startswith("https://yt3.ggpht.com"))

    def test_multi_image_post(self):
        """Test that posts with only multiple images are parsed correctly."""
        data = test_posts[4].data()
        self.assertEqual(data["postID"], "UgkxY2O9N8cX9rMNMK50lOK6VXMvw05uyTCa")
        self.assertEqual(data["contentText"], None)
        self.assertEqual(data["attachment"]["type"], "multiImage")
        self.assertTrue(data["attachment"]["URLs"][0].startswith("https://yt3.ggpht.com"))
        self.assertEqual(len(data["attachment"]["URLs"]), 5)

    def test_edited_post(self):
        """Test that edited posts have the edited attribute."""
        data = test_posts[5].data()
        self.assertEqual(data["postID"], "Ugkxh2DuCHmAmyjdAKVv_dcmrvMj787b2OL1")
        self.assertEqual(data["contentText"], "Test Post Edit")
        self.assertTrue(data["edited"])
        self.assertTrue(data["timeText"].endswith("ago"))

    def test_poll(self):
        """Test that posts with polls are parsed correctly."""
        data = test_posts[6].data()
        self.assertEqual(data["postID"], "UgkxQ2GoSAnhj3KbrWyvGVLLI16-oEcLJV2k")
        self.assertEqual(data["contentText"], "Test Post Text Poll")
        self.assertEqual(data["attachment"]["type"], "poll")
        self.assertTrue(data["attachment"]["votesText"].endswith("votes"))
        self.assertEqual(data["attachment"]["choices"],
            ["Choice One", "Choice Two", "Choice Three", "Choice Four"])
        self.assertEqual(data["attachment"]["imageURLs"], None)

    def test_image_poll(self):
        """Test that posts with image polls are parsed correctly."""
        data = test_posts[9].data()
        self.assertEqual(data["postID"], "UgkxWDZnrAVYI8w0jQOpRyC7XrJa9Ey_k1Wg")
        self.assertEqual(data["contentText"], "Image Poll")
        self.assertEqual(data["attachment"]["type"], "poll")
        self.assertTrue(data["attachment"]["votesText"].endswith("votes"))
        self.assertEqual(data["attachment"]["choices"], ["uwu", "owo"])
        self.assertTrue(data["attachment"]["imageURLs"][0].startswith("https://yt3.ggpht.com"))
        self.assertEqual(len(data["attachment"]["imageURLs"]), 2)

    def test_video_embed(self):
        """Test that posts with embedded videos are parsed correctly."""
        # This should be changed to a video on the test channel at some point
        data = test_posts[8].data()
        self.assertEqual(data["postID"], "Ugkx0mOGgVuFfy8znxJWfIdryu6XL2iQHdOu")
        self.assertEqual(data["contentText"], "Video Post")
        self.assertEqual(data["attachment"]["type"], "video")
        self.assertEqual(data["attachment"]["ID"], "dQw4w9WgXcQ")
        self.assertTrue(data["attachment"]["thumbnailURL"].startswith("https://i.ytimg.com"))
        self.assertEqual(data["attachment"]["title"],
            "Rick Astley - Never Gonna Give You Up (Official Music Video)")
        self.assertTrue(data["attachment"]["descriptionSnippet"].startswith("The official video"))
        self.assertEqual(data["attachment"]["authorDisplayName"], "Rick Astley")
        self.assertTrue(data["attachment"]["timeText"].endswith("years ago"))
        self.assertEqual(data["attachment"]["lengthText"], "3:33")
        self.assertTrue(data["attachment"]["viewCount"] >= 1462235415) # View count as of writing this
        self.assertTrue(data["attachment"]["viewCountText"].endswith("views"))

    def test_quiz(self):
        """Test that posts with quizzes are parsed correctly."""
        data = test_posts[7].data()
        self.assertEqual(data["postID"], "Ugkxj5sWVNGmEZE73g2zxSea8k89GlceOA1d")
        self.assertEqual(data["contentText"], "Test Post Quiz")
        self.assertEqual(data["attachment"]["type"], "quiz")
        self.assertEqual(data["attachment"]["choices"], ["Answer 1", "Answer 2", "Answer 3 (Correct)"])
        self.assertEqual(data["attachment"]["correctChoice"], 2)
        self.assertEqual(data["attachment"]["explanation"], "Explanation For Correct Answer")
        self.assertTrue(data["attachment"]["answerCountText"].endswith("answered"))

    def test_comment_count(self):
        """Test that the comment count of posts is correct."""
        data = test_posts[12].data()
        self.assertEqual(data["postID"], "UgkximjhpHrqqxHue2IDIpiDRDVK9Q3J8z4c")
        self.assertEqual(data["contentText"], "Test Post With Many Comments")
        self.assertEqual(data["commentCountText"], "43")
        self.assertEqual(test_posts[12].data()["commentCount"], 43)

    def test_vote_count(self):
        """Test that the vote count of posts is correct(ish)."""
        data = test_posts[13].data()
        self.assertEqual(data["postID"], "UgkxXrf-6FdrjY1oY5Og-2V8cm_Hmx1Zb8IS")
        self.assertEqual(data["contentText"], "Test Post With Vote")
        self.assertTrue(data["likeCount"] >= 1)

class TestComment(unittest.TestCase):
    """Test the Comment class (and by extension the parse_comment function)."""

    def test_no_comments(self):
        """Test that a post with no comments returns an empty array."""
        self.assertEqual(no_comments, [])

    def test_one_comment(self):
        """Test that a post with one comment is parsed correctly."""
        self.assertTrue(len(one_comment), 1)
        data = one_comment[0].data()
        self.assertEqual(data["authorID"], "UCSHozX8N-F7GygP9PIIYxLw")
        self.assertEqual(data["authorDisplayName"], "@CommunityDownTest")
        self.assertTrue(data["authorImageURL"].startswith("https://yt3.ggpht.com"))
        self.assertEqual(data["commentID"], "UgycOEolpmxD37kcJJN4AaABAg")
        self.assertTrue(data["likeCount"] >= 1)
        self.assertEqual(data["replyCount"], 0)
        self.assertTrue(data["timeText"].endswith("ago"))
        self.assertFalse(data["edited"])
        self.assertEqual(data["contentText"], "Hurdle Durdle")

    def test_comments(self):
        """Test comments from a post with multiple comments are fetched and parsed correctly."""
        # All the comments was fetched from the post
        self.assertEqual(len(top_comments), 35)
        self.assertEqual(len(chrono_comments), 35)
        comment1, comment2 = [c.data() for c in chrono_comments[0:2]]
        # Comment content and reply count is correct (for the first two comments at least)
        self.assertEqual(comment1["commentID"], "UgxmOxIaaaHFkH22tj94AaABAg")
        self.assertEqual(comment1["contentText"], "Hello")
        self.assertEqual(comment1["replyCount"], 3)
        self.assertEqual(comment2["commentID"], "UgzbF4D7-o3C9P2izEV4AaABAg")
        self.assertEqual(comment2["contentText"], "Test Test")

    def test_edited_comment(self):
        """Test an edited comment has the edited attribute."""
        data = chrono_comments[33].data()
        self.assertEqual(data["commentID"], "UgwWsiDrEvru2rp9M8Z4AaABAg")
        self.assertEqual(data["contentText"],
            "youtube api = stupid and i hate (edited nvm I love youtube api (jk))")
        self.assertEqual(data["replyCount"], 4)
        self.assertTrue(data["edited"])

    def test_complex_comment(self):
        """Test a complex comment (with emojis, links, and formatting) is parsed correctly."""
        data = chrono_comments[34].data()
        self.assertEqual(data["commentID"], "Ugw6VVsZhhzklrzJdMV4AaABAg")
        self.assertEqual(data["contentText"],
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

    def test_fetch_comments_limit(self):
        """Test Post.fetch_comments limit function returns correct comments."""
        limit0 = test_posts[12].fetch_comments(limit = 0)
        limit17 = test_posts[12].fetch_comments(limit = 17)
        limit32 = test_posts[12].fetch_comments(limit = 32)
        self.assertEqual(limit0, [])
        self.assertEqual(len(limit17), 17)
        self.assertEqual(len(limit32), 32)

        self.assertEqual([o.data()["commentID"] for o in limit17],
            [o.data()["commentID"] for o in limit32[-17:]])

unittest.main()
