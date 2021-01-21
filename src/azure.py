import adafruit_requests as requests
import ssl
import json
import wifi
import socketpool


class azure:

    def __init__(self, app_id, password, tennent_id, subscription_id):
        self._app_id = app_id
        self._password = password
        self._tennent_id = tennent_id
        self._subscription_id = subscription_id
        pool = socketpool.SocketPool(wifi.radio)
        self._https = requests.Session(pool, ssl.create_default_context())

    def _error_handler(self, error):
        print(error['error_description'])

    def _get_token(self):
        data = {'grant_type': 'client_credentials',
                'client_id': self._app_id,
                'client_secret': self._password,
                'resource': 'https://management.azure.com/'
                }
        url = 'https://login.microsoftonline.com/{}/oauth2/token'\
              .format(self._tennent_id)
        response = self._https.post(url, data=data)
        json_resp = response.json()
        try:
            token = json_resp["access_tokn"]
        except KeyError as error:
            self._error_handler(error)
            quit()

        return token

    def cost_forecast(self):
        with open('./requestbody.json') as f:
            data = json.load(f)

        token = self._get_token()
        headers = {'Authorization': 'Bearer ' + token}

        url = 'https://management.azure.com/subscriptions/{}/providers/Microsoft.CostManagement/forecast?api-version=2019-10-01'\
              .format(self._subscription_id)

        response = self._https.post(url, json=data, headers=headers)
        json_resp = response.json()
        try:
            cost_forecast = json_resp["properties"]["rows"][0][0]
        except Exception:
            self._error_handler(json_resp)
            quit()

        return cost_forecast
