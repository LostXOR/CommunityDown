"""Comment class! Pylint wants module docstrings, but since each module only has one class/function
and they already have docstrings it's kinda pointless. But I want to appease the Pylint gods. :)"""

from parse_comment import parse_comment

class Comment:
    """Class representing a comment on a community post."""
    def __init__(self, data):
        """Parse and store raw comment data as attributes of this object."""
        self.__raw_data = data
        self.__data = parse_comment(self.__raw_data)
        for key, value in self.__data.items():
            setattr(self, key, value)

    def data(self):
        """Return the parsed comment data as a dict"""
        return self.__data

    def raw_data(self):
        """Return the raw comment data as a dict"""
        return self.__raw_data