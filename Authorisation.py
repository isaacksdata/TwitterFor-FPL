from dotenv import load_dotenv
import os


class Authoriser:
    def __init__(self):
        self.bearerToken = None

    def resetToken(self):
        self.bearerToken = None

    def auth(self):
        try:
            load_dotenv()
            self.bearerToken = os.getenv('BEARER_TOKEN')
        except Exception:
            return False
        else:
            return self.bearerToken is not None

    def getBearerToken(self) -> str:
        return self.bearerToken
