from dotenv import load_dotenv
import os


class Authoriser:
    def __init__(self):
        self.bearerToken = None
        self.auth()

    def auth(self):
        load_dotenv()
        self.bearerToken = os.getenv('BEARER_TOKEN')

    def getBearerToken(self) -> str:
        return self.bearerToken
