import requests

servers = {
    "ru":"ru",
    "euw":"euw1",
    "eun":"eun1"
}
def get_riot_rank(nickname, server):
    REG_API = "RGAPI-cbdf51c5-5192-47bd-8693-757277daef30"

    base_url = "https://europe.api.riotgames.com"
    headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": REG_API
    }
    name, tag = nickname.split("#")

    responses = requests.get(base_url+f"/riot/account/v1/accounts/by-riot-id/{name}/{tag}",headers=headers)
    response_body = responses.json()
    if "puuid" not in response_body:
        return "Нет такого человечка"
    current_puuid = response_body["puuid"]

    response1 = requests.get(f"https://{servers[server]}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{current_puuid}",headers=headers)
    response_json1 = response1.json()
    if "id" not in response_json1:
        return "По ходу сервак не тот"
    current_id = response_json1["id"]
    current_account_id = response_json1["accountId"]
    current_summoner_level = response_json1["summonerLevel"]

    response_body3 = requests.get(f"https://{servers[server]}.api.riotgames.com/lol/league/v4/entries/by-summoner/{current_id}",headers=headers)
    response_json3 = response_body3.json()
    response_string = ""
    if len(response_json3)==0:
        return "Нет ранга"
    for i in response_json3:
        response_string += get_rank_by_queue(i)+"; "
    return response_string

def get_rank_by_queue(rank_obj):
    if rank_obj['queueType'].startswith("RANKED_SOLO"):
        return f"Solo: {rank_obj['tier']} {rank_obj['rank']}"
    else:
        return f"Flex: {rank_obj['tier']} {rank_obj['rank']}"
