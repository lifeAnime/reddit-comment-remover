import requests, time

auth = requests.auth.HTTPBasicAuth('L8SOtFFdaunpFA', '2Zau2eD-JyphePs13LQ0F1ak-npFGQ')
data = {'grant_type': 'password',
        'username': 'x',
        'password': 'x'}
headers = {'User-Agent': 'Py:Shredder:1.0 (by /u/hynauts)'}

def fetch_token(auth=auth, data=data, headers=headers):
    try:
        TOKEN = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers).json()['access_token'] # valid 2 hours
    except:
        print('Error during request of access_token.. Exiting program')
        return 'error'
    else:
        print('Successfully retrieved an access_token')
        return TOKEN

def edit_comment(headers, message_id):
    data = {"thing_id": f"{message_id}", "api_type": "json", "text": "!X01X03X01X! Message edited"}
    try:
        r = requests.post('https://oauth.reddit.com/api/editusertext', headers=headers, data=data)
    except Exception as e:
        print("request module error:", e)
        exit()
    else:
        if (r.status_code == 429):
            print(f"ratelimited. Program paused for {r.headers['X-Ratelimit-Reset']} seconds")
            time.sleep(int(r.headers['X-Ratelimit-Reset']))
            edit_comment(headers, message_id)
            return
        elif (r.status_code != 200):
            print(r.request.body, "\n", "HTTP Error",r.status_code)
            exit()

def delete_comment(headers, message_id):
    data = {"id": f"{message_id}"}
    try:
        r = requests.post('https://oauth.reddit.com/api/del', headers=headers, data=data)
    except Exception as e:
        print("request module error:", e)
        exit()
    else:
        if (r.status_code == 429):
            print(f"ratelimited. Program paused for {r.headers['X-Ratelimit-Reset']} seconds")
            time.sleep(int(r.headers['X-Ratelimit-Reset']))
            delete_comment(headers, message_id)
            return
        elif (r.status_code != 200):
            print(r.request.body, "\n", "HTTP Error",r.status_code)
            exit()

def check_comments(headers, message_list):
    EDIT_ERROR = 0
    length = len(message_list)
    if (length > 100):
        print("len > 100 ?")
        exit()
    craft = ""
    i = 0
    for x in message_list:
        i += 1
        craft += f"{x}"
        if (i < length):
            craft += ","
    try:
        r = requests.get(f'https://oauth.reddit.com/api/info?id={craft}', headers=headers)
    except Exception as e:
        print("request module error:", e)
        exit()
    else:
        if (r.status_code == 429):
            print(f"ratelimited. Program paused for {r.headers['X-Ratelimit-Reset']} seconds")
            time.sleep(int(r.headers['X-Ratelimit-Reset']))
            check_comments(headers, message_list)
            return 0
        elif (r.status_code != 200):
            print(r.request.body, "\n", "HTTP Error",r.status_code)
            exit()
    for x in r.json()['data']['children']:
        if (x['data']['body'] != "!X01X03X01X! Message edited"):
            edit_comment(headers, x['data']['name'])
            EDIT_ERROR += 1
    return EDIT_ERROR
