class DomainMessage:
    def __init__(self, from_user, to_user, content, timestamp, tags=None, is_read=False):
        
        self.from_user = from_user
        self.to_user = to_user
        self.content = content
        self.timestamp = timestamp
        self.tags = tags or []
        self.is_read = is_read