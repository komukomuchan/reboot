import requests


#プロキシ
KEY = ACCESS_CLASH_ROYALE_API_KEY



def access_api(mode,tag):
    access_key = KEY

    #9QL8QC09 (レコブラクランタグ)
    #P8RG0YGL トワストのクランタグ

    tag = tag.replace("#","%23")

    url = "https://proxy.royaleapi.dev/v1/{0}/{1}/".format(mode,tag)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'max-age=60',
        'authorization': 'Bearer  %s' % access_key}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Check for any HTTP errors
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        print("エラーが発生しました")
        print(e)
        return e




def access_search_clans(mode,tag):
    access_key = KEY

    #9QL8QC09 (レコブラクランタグ)
    #P8RG0YGL トワストのクランタグ

    tag = tag.replace("#","%23")

    url = "https://proxy.royaleapi.dev/v1/{0}?{1}".format(mode,tag)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'max-age=60',
        'authorization': 'Bearer  %s' % access_key}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Check for any HTTP errors

        data = r.json()
    except requests.exceptions.RequestException as e:
        print("エラーが発生しました")
        print(e)
        data = access_search_clans(mode,tag)

    if "reason" in data :
        if data["reason"] == 'accessDenied.invalidIp' :
            print("アクセスキーが違います")

    return data

def access_current_riverrace(tag):
    access_key = KEY


    tag = tag.replace("#","%23")

    url = "https://proxy.royaleapi.dev/v1/clans/{0}/currentriverrace".format(tag)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'max-age=60',
        'authorization': 'Bearer  %s' % access_key}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Check for any HTTP errors

        data = r.json()
    except requests.exceptions.RequestException as e:
        print("エラーが発生しました")
        print(e)

    return data


def access_local_ranking():
    access_key = KEY

    url = "https://proxy.royaleapi.dev/v1/locations/57000122/pathoflegend/players"
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'max-age=60',
        'authorization': 'Bearer  %s' % access_key}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Check for any HTTP errors
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        print("エラーが発生しました")
        print(e)
        return e
