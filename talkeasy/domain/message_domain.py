from api.message_schemas import MessageOutSender

class DomainMessage:
    def __init__(self, from_user, to_user, content, timestamp, tags=None, is_read=False, id=None):
        self.id = id
        self.from_user = from_user
        self.to_user = to_user
        self.content = content
        self.timestamp = timestamp
        self.tags = tags or []
        self.is_read = is_read

    def as_dict(self):
        return {
            "id": self.id,
            "from_user": self.from_user,
            "to_user": self.to_user,
            "content": self.content,
            "timestamp": self.timestamp,
            "tags": self.tags,
            "is_read": self.is_read
        }