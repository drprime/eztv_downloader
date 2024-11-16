import json
import requests
import os
from lxml import html
from magnet2torrent import magnet2torrent
from dotenv import load_dotenv

load_dotenv()

def find_movie(imdb_id, api_key, enable_logs = False):
    code = "(async () => { let req = await fetch(\"https://en.eztv-official.com/ajax/search?query=" + imdb_id + "\"); let result = await req.json(); if(result.status ===\"ok\"){let url = result.data[0].url; req = await fetch(url); result = await req.text()} })()"
    scenario = [
        {"wait_for": "#main-search-fields"},
        {"evaluate" : code}
    ]

    params = {
        "apikey" : api_key,
        "url" : "https://en.eztv-official.com/movies",
        "js_render" : "true",
        "json_response" : "true",
        "js_instructions" :  json.dumps(scenario)
    }

    res = requests.get(url="https://api.zenrows.com/v1/", params=params)
    answer = res.json()
    if "xhr" not in answer:
        if(enable_logs):
            print(answer)
        return {"status": "error", "message": "Request error"}
    
    search_res = list(filter(lambda x: "/ajax/search?query=" in x["url"], answer["xhr"]))
    if len(search_res) == 0:
        if(enable_logs):
            print(answer)
        return {"status": "error", "message": "Request error"}

    search_res_body = search_res[0]["body"]
    search_res_json = json.loads(search_res_body)

    if search_res_json["status"] != "ok":
        if(enable_logs):
            print(answer)
        return {"status": "error", "message": "Movie not found"}

    search_res_url = search_res_json["data"][0]["url"]
    movie_res = list(filter(lambda x:  search_res_url in x["url"], answer["xhr"]))
    if len(movie_res) == 0:
        if(enable_logs):
            print(answer)
        return {"status": "error", "message": "Request error"}

    movie_res_body = movie_res[0]["body"]    
    tree = html.fromstring(movie_res_body)
    quality_list = tree.xpath('//table/tbody/tr/td[1]/text()')
    names_list = tree.xpath('//table/tbody/tr/td[2]/text()')
    url_list = tree.xpath('//table/tbody/tr/td[4]/a/@href')

    movie_obj = []
    iterator = -1
    for quality in quality_list:
        iterator += 1
        temp_obj = {
            "quality" : quality,
            "name" : names_list[iterator],
            "url" : url_list[iterator]
        }
        movie_obj.append(temp_obj)
    return {"status" : "ok", "result" : movie_obj }



if __name__ == "__main__":
    api_key = os.getenv("ZENROWS_API_KEY")
    save_path = os.getenv("EZTV_SAVE_PATH")
    id_list_file = os.getenv("EZTV_ID_LIST")
    
    with open(id_list_file, "r") as f:
        id_list = f.read().splitlines() 
    
    while len(id_list) > 0:
        imdb_id = id_list[0]
        print("IMDB id " + imdb_id)
        is_torrent_exists = os.path.exists(save_path + imdb_id + ".torrent")
        if(not is_torrent_exists):
            result = find_movie(imdb_id, api_key, True)
            print("Status: " + result["status"])
            if result["status"] == "ok":
                torrent_url  = result["result"][0]["url"]
                print(torrent_url)
                is_success = magnet2torrent(torrent_url, save_path + imdb_id + ".torrent")
                if(not is_success):
                    id_list.append(imdb_id)
            else:
                print(result["message"])
                if result["message"] == "Request error":
                    id_list.append(imdb_id)

        #Update file
        id_list = id_list[1:]
        with open(id_list_file, 'w') as f:
            f.write("\n".join(id_list))