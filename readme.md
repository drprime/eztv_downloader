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

### 5. Setup variables

Zenrows api key

```python
api_key = "..."
```

Save path for .torrent files

```python
save_path = "./torrent_files/2020-2024/"
```

Path to file with imdb id list

```python
id_list_file = "id_list.txt"
```

### 6. Run script
```sh
python3 eztv_downloader.py
```


## imdb id scraping
### 1. Setup variables in file tmdb_get_ids.py

You can change scraping filters in ``params`` object

```python
vote_average.gte #minimal rating 
vote_average.lte #maximum rating 
with_origin_country #country list with "|" separator
```

Setup save file

```python
save_file = 'id_list.txt'
```

Setup years range

```python
years = range(2020, 2025) #range from 2020 to 2024
years = [2020] #only 2020
```

Setup tmdb access token

```python
tmdb_access_token = "..."
```

Setup threads num

```python
MAX_THREADS = 12
```

### 2. Run script
```sh
python3 tmdb_get_ids.py
```