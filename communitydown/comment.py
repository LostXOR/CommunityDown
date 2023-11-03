"""Comment class! Pylint wants module docstrings, but since each module only has one class/function
and they already have docstrings it's kinda pointless. But I want to appease the Pylint gods. :)"""

import communitydown

class Comment:
    """Class representing a comment on a community post."""
    def __init__(self, data):
        """Parse and store raw comment data as attributes of this object."""
        self.__raw_data = data
        self.__data = communitydown.parse_comment_data(data)

    def data(self):
        """Return the parsed comment data as a dict"""
        return self.__data

    def raw_data(self):
        """Return the raw comment data as a dict"""
        return self.__raw_data

    def fetch_replies(self, chronological = False, limit = -1):
        return [] # Unimplemented