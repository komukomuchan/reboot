import requests


#プロキシ
KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImVmNzU2NjY2LTM1MWEtNDc0Zi1hYTZjLTA4ZjNhZTI3YzgyYyIsImlhdCI6MTY5Mzc0ODY1OCwic3ViIjoiZGV2ZWxvcGVyLzVjMTk1OThiLWY5ODctNDY4Ni03ZWIwLWQ3ZGRhNWViMzAyZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS43OS4yMTguNzkiXSwidHlwZSI6ImNsaWVudCJ9XX0.S1FO1-jLNBCy4T86Y4XCuJ9lMcnq6_atovVx-4eSCVIrDEfxy573gF4aW65kQFPTx0n56tPaW3_vF7Hw06a3cA"



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
