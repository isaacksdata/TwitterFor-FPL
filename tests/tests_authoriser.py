import unittest

from Authorisation import Authoriser


class TestUtilityFunctions(unittest.TestCase):
    def setUp(self):
        print('--------------------------------------\n'
              '---------- Testing Authoriser -----------------\n'
              '-----------------------------------------------')
        self.authoriser = Authoriser()

    def test_resetToken(self):
        print('---------- Testing resetToken -----------------')
        self.authoriser.resetToken()
        self.assertIsNone(self.authoriser.bearerToken, 'Failed to set token to None')

    def test_auth(self):
        print('---------- Testing auth -----------------')
        response = self.authoriser.auth()
        self.assertTrue(response, 'Failed to get authorisation token')

    def test_getBearerToken(self):
        self.authoriser.resetToken()
        self.assertIsNone(self.authoriser.getBearerToken(), 'Bearer token is not None even after reset')

        _ = self.authoriser.auth()
        self.assertIsNotNone(self.authoriser.getBearerToken(), 'Bearer token is None after auth()')