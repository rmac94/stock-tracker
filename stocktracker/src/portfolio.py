from dataclasses import dataclass
import json, os, misc

project_path = misc.project_path()

@dataclass
class track:
    ticker: str
    timestamp: int
    action: str
        
    def _create_activity_log(self):
        cls_type = self.__class__.__name__
        try:
            os.mkdir(os.path.join(os.path.expanduser('~'), 'stock-data'))
            with open(f'{project_path}\\data\\{cls_type}-log.json', 'x') as f:
                header = f'{{"{cls_type}":[]}}'
                f.write(header)
                f.close()
        except FileExistsError:
            pass
        
    def _log_activity(self):
        return(vars(self))
    
    def save_log(self):
        cls_type = self.__class__.__name__
        self._create_activity_log()
        activity = self._log_activity()
        with open(os.path.join(os.path.expanduser('~'), 'stock-data', f'{cls_type}-log.json'),"r+") as file:
            data = json.load(file)
            data[f'{cls_type}'].append(activity)
            file.seek(0)
            json.dump(data, file)

@dataclass
class transaction(track):
    shares: float
        
    def execution_stock_price(self):
        pass
    
    def execution_transaction_value(self):
        pass
