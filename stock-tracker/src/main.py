import time, json
import portfolio as pf
import stock as s
import glob


def create_portfolio():
    if not glob.glob(pf.project_path + '\\data'):
        portfolio = ["gxo", "googl", "msft", "atkr", "pltr", "qcom", "brk.b", "orcl", "wfc", "pypl", "jpm", "lpx", "csl"]
        portfolio = [[k, int(time.time()), "track"] for k in portfolio]
        for stock in portfolio:
            action = pf.track(stock[0], stock[1], stock[2])
            action.save_log()


def read_portfolio_data(partition):
    with open(f'{pf.project_path}/data/track-log.json', "r+") as file:
        for x in json.load(file)[f'{partition}']:
            yield x


def update_portfolio_data(partition):
    for x in read_portfolio_data(partition):
        s.stock(ticker=x['ticker'], timestamp=x['timestamp']).get_update()


def main():
    update_portfolio_data('track')


if __name__ == "__main__":
    main()



