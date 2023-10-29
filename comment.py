from parse_comment import parse_comment

class Comment:
    def __init__(self, data):
        # Parse and store comment's data in this object
        self.raw_data = data
        self.data = parse_comment(self.raw_data)
        for key in self.data:
            setattr(self, key, self.data[key])
