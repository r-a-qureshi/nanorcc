from zipfile import ZipFile
from os.path import exists
from os import remove
from urllib.request import urlretrieve

def download_sample_files(
    targetdir,
    url='https://www.nanostring.com/download_file/view/1190/3842',
):
    """Download and extract sample data from nanostring website"""
    if exists(targetdir):
        pass
    else:
        raise FileNotFoundError(targetdir)
    data,response = urlretrieve(url) 
    compressed = ZipFile(data)
    compressed.extractall(path=targetdir)
    compressed.close()
    remove(data)
