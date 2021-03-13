import requests, json, time
import utils

auth = utils.auth
data = utils.data
headers = utils.headers
TOKEN = utils.fetch_token(auth, data, headers)
TOTAL_MESSAGE = 0
EDIT_ERROR = 0
message_list = []
headers = {'User-Agent': 'Py:Shredder:1.0 (by /u/hynauts)', 'Authorization': f"bearer {TOKEN}"}

if (TOKEN == 'error'):
    exit()

while (1):
    try:
        r = requests.get(f'https://oauth.reddit.com/user/hynauts/comments?limit=100', headers=headers)
    except Exception as e:
        print("requests module error :",e)
        exit()
    if (r.status_code == 429):
            while (r.headers['X-Ratelimit-Remaining'] == 0):
                print(f"ratelimited. {r.headers['X-Ratelimit-Reset']} seconds to go")
                time.sleep(1)
            continue
    elif (r.status_code != 200):
        print(r.request.body, "\n", "HTTP Error",r.status_code)
        exit()
    dist = r.json()['data']['dist'] 
    if (dist == 0):
        break
    for x in r.json()['data']['children']:
        message_list.append(x['data']['name'])
    for message_id in message_list:
        print(f"[EDITING] Messages edited : {TOTAL_MESSAGE}",f"Edits errors : {EDIT_ERROR}" if (EDIT_ERROR > 0) else "",  "                                 ", end="\r")
        utils.edit_comment(headers, message_id)
        TOTAL_MESSAGE += 1
    print(f"[CHECKING] Messages edited : {TOTAL_MESSAGE}",f"Edits errors : {EDIT_ERROR}" if (EDIT_ERROR > 0) else "",  "                                 ", end="\r")
    EDIT_ERROR += utils.check_comments(headers, message_list)
    for message_id in message_list:
        print(f"[REMOVING] Messages edited : {TOTAL_MESSAGE}",f"Edits errors : {EDIT_ERROR}" if (EDIT_ERROR > 0) else "",  "                                 ", end="\r")
        utils.delete_comment(headers, message_id)
    message_list = []
    print (f"\n dist = {dist} & ",r.json()['data']['children'][0]['data']['name'],"\n")
print(f"\n Task completed. Comments deleted : {TOTAL_MESSAGE} Edits errors : {EDIT_ERROR}")