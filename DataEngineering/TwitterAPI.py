import requests
import datetime
import time

from DataEngineering.Authorisation import Authoriser


class TwitterAPI:
    def __init__(self):
        self.bearerToken = None
        self.start_time = datetime.datetime.today() - datetime.timedelta(days=6.5)
        self.start_time = self.start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        self.end_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        time.sleep(15)

    def auth(self):
        auth = Authoriser()
        _ = auth.auth()
        token = auth.getBearerToken()
        if token is not None:
            self.bearerToken = token
        else:
            raise ValueError('Failed to authorise!')

    def createHeaders(self, bearer_token: str) -> dict:
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def createUrl(self, keyword: str, start_date: str, end_date: str, max_results: int = 10) -> tuple:
        search_url = "https://api.twitter.com/2/tweets/search/recent"  # Change to the endpoint you want to collect data from

        # change params based on the endpoint you are using
        query_params = {'query': keyword,
                        'start_time': start_date,
                        'end_time': end_date,
                        'max_results': max_results,
                        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                        'next_token': {}}
        return (search_url, query_params)

    def connectToEndpoint(self, url: str, headers: dict, params: dict, next_token: str = None) -> dict:
        params['next_token'] = next_token  # params object received from create_url function
        response = requests.request("GET", url, headers=headers, params=params)
        print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            print(f'ERROR : {response.status_code}, :  {response.text}\nMinusing an hour' )
            d = datetime.datetime.strptime(params['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            newD = d - datetime.timedelta(hours=1)
            params['end_time'] = newD.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            response = requests.request("GET", url, headers=headers, params=params)
            print("Endpoint Response Code: " + str(response.status_code))
        return response.json()

    def getKeyword(self, query: str = None) -> str:
        if query is None:
            print('Input a player name : ')
            query = input()
        return query

    def makeQuery(self, query: str = None, nextToken: str = None) -> tuple:
        self.auth()
        headers = self.createHeaders(self.bearerToken)
        # keyword = "ronaldo FPL lang:en"
        k = self.getKeyword(query)
        keyword = f'{k} FPL lang:en'
        max_results = 100
        url = self.createUrl(keyword, self.start_time, self.end_time, max_results)
        json_response = self.connectToEndpoint(url[0], headers, url[1], nextToken)
        return (json_response, k)


if __name__ == '__main__':
    api = TwitterAPI()
    api.makeQuery()


