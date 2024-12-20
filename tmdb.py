import requests

class TMDB():
    def __init__(self, access_token):
        self.api_endpoint = "https://api.themoviedb.org/3/"
        self.access_token = access_token
        self.params = {
            "language": "en-US",
            "sort_by" : "popularity.desc"
        }
        self.headers = {
            "Authorization" : "Bearer " + access_token
        }
    def discover(self, params, enable_log=False):
        for key in self.params.keys():
            params[key] = self.params[key]
        response = requests.get(self.api_endpoint + "discover/movie", params=params, headers=self.headers)
        res = response.json()
        if enable_log:
            print(res)
        if "success" in res and not res["success"]:
           raise Exception(res["status_message"])
        return res
    def external_ids(self, id, enable_log=False):
        response = requests.get(self.api_endpoint + f"movie/{id}/external_ids", headers=self.headers)
        res = response.json()
        if enable_log:
            print(res)
        if "success" in res and not res["success"]:
           raise Exception(res["status_message"])
        return res