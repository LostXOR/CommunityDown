from parse_comment import parse_comment

class Comment:
    """Class representing a comment on a community post."""
    def __init__(self, data):
        """Parse and store raw comment data as attributes of this object."""
        self.raw_data = data
        self.data = parse_comment(self.raw_data)
        for key, value in self.data.items():
            setattr(self, key, value)
