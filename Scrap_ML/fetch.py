import os
import tarfile
import urllib.request

download_Root = "https://github.com/ageron/handson-ml2/blob/master/" # this line had to be edited with githubs modified url format
housing_Path = os.path.join("../datasets", "housing")
housing_Url = download_Root + "datasets/housing/housing.tgz?raw=true" # this as well, from the original textbook

def fetch_housing_data(housing_url=housing_Url, housing_path = housing_Path):
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

fetch_housing_data()

