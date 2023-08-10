import unittest

from DataEngineering.FplApi import FplData


class TestUtilityFunctions(unittest.TestCase):
    def setUp(self):
        print('--------------------------------------\n'
              '---------- Testing FplApi -----------------\n'
              '-----------------------------------------------')
        self.myFpl = FplData()

    def test_constructor(self):
        print('---------- Testing constructor-----------------')
        self.assertIsNone(self.myFpl.data, 'Data is not None after init')
        self.assertIsNone(self.myFpl.playerNames, 'Player names not None after init')
        self.assertEqual(self.myFpl.baseUrl, 'https://fantasy.premierleague.com/api/', 'Incorrect base URL')

    def test_setUrl(self):
        print('---------- Testing setUrl -----------------')
        newUrl = 'https://thisismynewurl.com'
        self.myFpl.setUrl(newUrl)
        self.assertEqual(self.myFpl.baseUrl, newUrl, 'Failed to set new url')

    def test_getUrl(self):
        print('---------- Testing getUrl -----------------')
        self.assertEqual(self.myFpl.getUrl(), 'https://fantasy.premierleague.com/api/', 'Incorrect base url')

    def test_getDataFromEndpoint(self):
        print('---------- Testing getDataFromEndpoint -----------------')
        response = self.myFpl.getDataFromEndpoint()
        self.assertEqual(len(response['teams']), 20, 'Response did to not return 20 teams')

    def test_dict2Pandas(self):
        print('---------- Testing dict2Pandas -----------------')
        response = self.myFpl.getDataFromEndpoint()
        expectedPlayers = len(response['elements'])
        expectedCols = len(response['elements'][0])
        data = self.myFpl.dict2pandas(response)
        self.assertEqual(data.shape[0], expectedPlayers, 'Unexpected number of rows')
        self.assertEqual(data.shape[1], expectedCols, 'Unexpected number of columns')

    def test__getPlayerNames(self):
        print('---------- Testing getPlayerNames -----------------')
        response = self.myFpl.getDataFromEndpoint()
        expectedPlayers = len(response['elements'])
        data = self.myFpl.dict2pandas(response)
        names = self.myFpl.getPlayerNamesFromPandas(data)
        self.assertTrue(isinstance(names, list),  'Did not return expected list type')
        self.assertEqual(len(names), expectedPlayers, 'Unexpected number of players returned')


