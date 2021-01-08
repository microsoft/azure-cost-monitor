import adafruit_requests as requests
import ujson as json


class azure:

    def __init__(self, app_id, password, tennent_id, subscription_id):
        self._app_id = app_id
        self._password = password
        self._tennent_id = tennent_id
        self._subscription_id = subscription_id

    def _get_token(self):
        print('getting token')
        data = {'grant_type': 'client_credentials',
                'client_id': self._app_id,
                'client_secret': self._password,
                'resource': 'https://management.azure.com/'
                }
        url = 'https://login.microsoftonline.com/{}/oauth2/token'\
              .format(self._tennent_id)
        response = requests.post(url, data=data)
        json_resp = response.json()
        token = json_resp["access_token"]
        return token

    def cost_forecast(self):
        with open('./requestbody.json') as f:
            data = json.load(f)

        token = self._get_token()
        headers = {'Authorization': 'Bearer ' + token}

        url = 'https://management.azure.com/subscriptions/{}/providers/Microsoft.CostManagement/forecast?api-version=2019-10-01'\
              .format(self._subscription_id)
        response = requests.post(url, json=data, headers=headers)
        json_resp = response.json()
        # TODO Check for valid response
        cost_forecast = json_resp["properties"]["rows"][0][0]
        return cost_forecast
