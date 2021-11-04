from dataclasses import dataclass
from pathlib import Path
import json, os, time, socket, pathlib, socket 

project_path = str(pathlib.Path(os.path.abspath('')).parent)
if socket.gethostname() == 'Test3':
    project_path = str(os.path.join(Path(os.path.abspath('')),'stock-tracker'))

@dataclass
class track:
    ticker: str
    timestamp: int
    action: str
        
    def _create_activity_log(self):
        cls_type = self.__class__.__name__
        try:
            os.mkdir(f'{project_path}\\data')
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
        with open(f'{project_path}/data/{cls_type}-log.json',"r+") as file:
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
