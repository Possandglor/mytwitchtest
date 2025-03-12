import requests

def generate_fact():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://castlots.org',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://castlots.org/generator-interesnykh-faktov/',
        'Priority': 'u=0',
    }

    data = {
        'hid': 'yes',
    }

    result = requests.post("http://castlots.org/generator-interesnykh-faktov/generate.php", headers=headers, data=data)
    return result.json()["va"]


def generate_status():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://castlots.org',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://castlots.org/generator-citat-online/',
        'Priority': 'u=0',
    }

    data = {
        'hid': 'yes',
    }

    result = requests.post("http://castlots.org/generator-citat-online/generate.php", headers=headers, data=data)
    return result.json()["va"]

def generate_anekdot():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://castlots.org',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://castlots.org/generator-anekdotov-online/',
        'Priority': 'u=0',
    }

    data = {
        'hid': 'yes',
    }

    result = requests.post("http://castlots.org/generator-anekdotov-online/generate.php", headers=headers, data=data)
    return result.json()["va"]