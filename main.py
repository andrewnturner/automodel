from model import Model, StringField, ModelField


class User(Model):
    username = StringField()
    email = StringField()


class DataRequest(Model):
    request_id = StringField()
    user = ModelField(User)

    def say_hello(self):
        print(f"Hello {self.user.username}!")


if __name__ == "__main__":
    message = {
        "request_id": "12345",
        "user": {"username": "John", "email": "john@example.com"},
    }

    data_request = DataRequest.from_dict(message)

    data_request.say_hello()
