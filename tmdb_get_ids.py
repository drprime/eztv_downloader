import tmdb
from multiprocessing.pool import ThreadPool
import os
from dotenv import load_dotenv

load_dotenv()

def create_date_ranges(years):
    dates = []
    for year in years:
        year = str(year)
        for month in range(1,12):
            start_month = "0" + str(month) if month <= 9 else str(month)
            end_month = "0" + str(month+1) if month+1 <= 9 else str(month+1)
            dates.append({"start_date": f"{year}-{start_month}-01", "end_date" : f"{year}-{end_month}-01"})
        dates.append({"start_date": f"{year}-12-01", "end_date" : f"{year}-12-31"})
    return dates


def get_imdb_ids(date_range):
    msg_range = date_range["start_date"] + "-" + date_range["end_date"]
    print(f"New thread started with range {msg_range}")
    page = 0
    params["primary_release_date.gte"] = date_range["start_date"]
    params["primary_release_date.lte"] = date_range["end_date"]

    while True:
        page += 1
        print(f"Date range {msg_range}. Page {str(page)}")
        params["page"] = page
        res = tmdb_api.discover(params,enable_log)
        if len(res["results"]) == 0:
            break
        for movie in res["results"]:
            res_id = tmdb_api.external_ids(movie["id"], enable_log)
            if res_id["imdb_id"] is not None:
                results.append(res_id["imdb_id"])


def multithreading_run(dates):
    pool = ThreadPool(processes=MAX_THREADS)
    threads = []
    while(dates):
        date = dates.pop(0)
        threads.append(pool.apply_async(get_imdb_ids, (date,)))

    pool.close()
    pool.join()


results = []

params = {
    #"vote_average.gte" : 3.5 #vote min
    #"vote_average.lte" : 4.5 #vote max
    "with_origin_country" : "AT|BE|BG|HR|CY|CZ|DK|EE|FI|FR|DE|GR|HU|IE|IT|LV|LT|LU|MT|NL|PL|PT|RO|SK|SI|ES|SE|AL|AD|AM|BY|BA|FO|GE|GI|IS|IM|LI|MK|MD|MC|ME|NO|RU|SM|RS|CH|UA|GB|US"
}


yaars_settings = os.getenv("TMDB_YEARS")
save_file = os.getenv("TMDB_SAVE_FILE")
tmdb_access_token = os.getenv("TMDB_ACCESS_TOKEN")
enable_log = os.getenv("TMDB_ENABLE_LOGS") == "true"
MAX_THREADS = int(os.getenv("TMDB_MAX_THREADS")) 


years = range(int(yaars_settings.split("-")[0]), int(yaars_settings.split("-")[1]) + 1) if "-" in yaars_settings else [int()]

dates = create_date_ranges(years)
tmdb_api = tmdb.TMDB(tmdb_access_token)

multithreading_run(dates)

with open(save_file, 'w') as f:
    f.write("\n".join(results))
