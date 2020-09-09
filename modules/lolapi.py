#import Bot
import requests
#import Moduleloader
#import ts3.Events as Events
import json
from utility import parse_json, save_to_json, read_from_json, wipe_json_file

api_key = "RGAPI-affc40b1-2aa4-465d-90f7-1b898d3ed409"
BASE_URL = "https://{server}.api.riotgames.com/lol/"

servers = ["euw1"]
    

# data
summoner_name = "silentlama"
region = "europe"


# calls
get_account_id_by_name = "/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
get_summoner_id = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"



#region requests

def make_summoner_details_request(region, summoner_name, api_key):
    response = requests.get(f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}")
    return parse_json(response)


def make_active_game_request(summoner_id):
    response = requests.get(f"/lol/spectator/v4/active-games/by-summoner/{summoner_id}")
    return response.json

#endregion


class Summoner():
    def __init__(self, id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel):
        self.id = id
        self.accountId = accountId
        self.puuid = puuid
        self.name = name
        self.profileIconId = profileIconId
        self.revisionDate = revisionDate
        self.summonerLevel = summonerLevel

    def __str__(self):
        return self.name




def main():
    print(make_summoner_details_request(servers[0], "silentlama", api_key))


if __name__ == "__main__":
    main()