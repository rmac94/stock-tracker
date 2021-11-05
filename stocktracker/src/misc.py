from requests import get
import os, pathlib, glob, socket

def cloud_provider():
    if "microsoft" in get('https://ipinfo.io').json()['org'].lower():
        return True

def project_path():
    if cloud_provider():
        return str(os.path.join(pathlib.Path(os.path.abspath('')),'stocktracker'))
    return str(pathlib.Path(os.path.abspath('')).parent)

def credentials_check():
    files = glob.glob(str(pathlib.Path(project_path().parent))+'/*')
    return [True for x in files if 'credentials' in x][0]
    

def read_credentials():
    cred_path = os.path.join(str(pathlib.Path(os.path.abspath('')).parent.parent), 'credentials.ini')
    if socket.gethostname() == 'Test3':
        cred_path = os.path.join(str(pathlib.Path(os.path.abspath(''))), 'credentials.ini')


if __name__ == "__main__":
    print(1)




