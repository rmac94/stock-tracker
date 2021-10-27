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


def update_portfolio():
    with open(f'{pf.project_path}/data/track-log.json', "r+") as file:
        for x in json.load(file)['track']:
            s.stock(ticker=x['ticker'], timestamp=x['timestamp']).get_update()


def main():
    create_portfolio()
    update_portfolio()


if __name__ == "__main__":
    main()



