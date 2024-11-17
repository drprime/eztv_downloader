# eztv downloader

## .torrent files downloading

### 1. Install python3.10 with venv

```sh
sudo apt-get install python3.7-dev python3.7-venv
```

If you'll get errors like: E: Couldn’t find any package by glob ‘python3.10’ , stating that the packages can not be installed
run the following commands below, then re-run the install command above:

```sh
apt update
```

```sh
sudo apt install software-properties-common
```

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
```

### 2. Find out where your python 3.10 is located by this command:

```sh
which python3.10
```
Should be something like /usr/bin/python3.10

### 3. Create Virtual Environment in the Home directory.
```sh
cd
```

```sh
mkdir virtual_env
```

```sh
/usr/bin/python3.10 -m venv ~/virtual_env/venv_310
```

```sh
source ~/virtual_env/venv_30/bin/activate
```

### 4. Install libtorrent and lxml

```sh
pip install libtorrent lxml
```

### 5. Setup variables in .env file

Zenrows api key

```env
ZENROWS_API_KEY = ...
```

Save path for .torrent files

```env
EZTV_SAVE_PATH = ./torrent_files/2020-2024/
```

Path to file with imdb id list

```env
EZTV_ID_LIST = id_list.txt
```

### 6. Run script
```sh
python3 eztv_downloader.py
```


## imdb id scraping
### 1. Setup variables in .env file
You can change scraping filters in ``params`` object in script body

```python
vote_average.gte #minimal rating 
vote_average.lte #maximum rating 
with_origin_country #country list with "|" separator
```

Setup save file

```env
TMDB_SAVE_FILE = id_list_test.txt
```

Setup years range

```env
TMDB_YEARS = 2020-2021
TMDB_YEARS = 2020
```

Setup tmdb access token

```env
TMDB_ACCESS_TOKEN = ...
```

Setup threads num

```env
TMDB_MAX_THREADS = 8
```

Enable or disable responde logging

```env
TMDB_ENABLE_LOGS = false
TMDB_ENABLE_LOGS = true
```


### 2. Run script
```sh
python3 tmdb_get_ids.py
```