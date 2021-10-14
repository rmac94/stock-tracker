from pathlib import Path
import datetime, json, os, time
import stock

log = str(Path(os.path.abspath('')).parent) + '/data/track-log.json'

if __name__ == "__main__":

    # with open(log, 'r') as f:
    #     data = json.load(f)
    #     f.close()
    #
    # for item in data['track']:
    #     if item['action'] == 'track':
    #         try:
    #             stock.stock(item['ticker']).get_update()
    #             print(f"Updated {item['ticker']}")
    #         except:
    #             pass

    stock.stock("gxo").get_update()