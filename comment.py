from parsecomment import parseComment

class Comment:
    def __init__(self, data):
        # Parse and store comment's data in this object
        self.rawData = data
        self.data = parseComment(self.rawData)
        for key in self.data:
            setattr(self, key, self.data[key])
