import json, time, glob, requests, re, os
import pandas as pd
from datetime import datetime
import configparser
from pathlib import Path

cred_path = str(Path(os.path.abspath('')).parent.parent) + '/credentials.ini'
credentials = configparser.ConfigParser()
credentials.read(cred_path)


class stock:
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/"

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': credentials['DEFAULT']['key']
    }

    project_path = str(Path(os.path.abspath('')).parent)

    def __init__(self, ticker, region="US"):
        self.ticker = ticker
        self.region = region

    def get_price_history(self, interval='10m', data_range='28d', period1=None, period2=None):
        self.interval = interval
        self.data_range = data_range
        self.period1 = period1
        self.period2 = period2

        request_url = self.url + 'stock/v2/get-chart'

        parameters = {"interval": self.interval,
                      "symbol": self.ticker,
                      "region": self.region}

        if period1 == period2 == None:
            parameters = {**parameters, 'range': self.data_range}
        else:
            parameters = {**parameters, 'period1': self.period1, 'period2': self.period2}

        response = requests.request("GET", request_url, headers=self.headers, params=parameters)

        if response.status_code != 200 or response.json()['chart']['error']:
            raise Exception('Bad Request! ' + response.json()['chart']['error']['description'])

        main_body = response.json()['chart']['result'][0]
        data_points = pd.DataFrame(main_body['indicators']['quote'][0])

        data_points['time_stamp'] = main_body['timestamp']
        data_points['time'] = [datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S') for x in
                               main_body['timestamp']]

        return data_points[['time_stamp', 'time', 'volume', 'open', 'close', 'low', 'high']]

    def _initial_history(self):
        intervals = {'5m': '1mo',
                     '1d': '1y'}
        for interval, date_range in intervals.items():
            init = self.get_price_history(interval=f'{interval}', data_range=f'{date_range}')
            init.to_csv(f'{self.project_path}/data/{self.ticker}-price-history-{interval}.csv', index=False)

    def _get_history(self):
        files = glob.glob(f'{self.project_path}/data')
        return [file for file in files if f'{self.ticker}' in file]

    def _run_history(self):
        if not self._get_history():
            self._initial_history()

    def _intervals(self):
        ticker_files = self._get_history()
        return [re.findall(r"([0-9][dmy]).csv", period)[0] for period in ticker_files]

    def get_update(self):
        self._run_history()
        intervals = self._intervals()
        for interval in intervals:
            history = pd.read_csv(f'{self.project_path}/data/{self.ticker}-price-history-{interval}.csv') \
                [['time_stamp', 'time', 'volume', 'open', 'close', 'low', 'high']]
            period1 = history.time_stamp.max()
            period2 = int(time.time())
            data = self.get_price_history(interval=f'{interval}', period1=period1, period2=period2)
            update = pd.concat([history, data])
            update.to_csv(f'{self.project_path}/data/{self.ticker}-price-history-{interval}.csv', index=False)
