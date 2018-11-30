class DataRequest:
    def __init__(self, request_id, user):
        self.request_id = request_id
        self.user = user

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["request_id"],
            data["user"]
        )

    def as_dict(self):
        return {
            "request_id": self.request_id,
            "user": self.user.as_dict()
        }

    def say_hello(self):
        print(f"Hello {self.user.username}!")