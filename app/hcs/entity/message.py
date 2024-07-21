import json


class MessageEntity:
    @staticmethod
    def get(body):
        return json.dumps({"message": body})
