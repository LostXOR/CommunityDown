from parsepost import parsePost

class Post:
    def __init__(self, data):
        # Parse post data
        self.data = parsePost(data)
        for key in self.data:
            setattr(self, key, self.data[key])