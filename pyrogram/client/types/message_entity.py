class MessageEntity:
    def __init__(self,
                 type: str,
                 offset: int,
                 length: int,
                 url: str = None,
                 user: "User" = None):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
