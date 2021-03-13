# reddit-comment-remover

First you need Python and these packages : requests, json, time
Then you need to edit the 'auth' and 'data' dicts in utils.py, here is an example of how they should look :

```python
auth = requests.auth.HTTPBasicAuth('oUrAATyGe6fczs', '6Bau2eD-JyphePs26LQ0F1ao-bnFGC')
data = {'grant_type': 'password',
        'username': 'HoloDragon3232',
        'password': 'Basicpassword123'}
```
To get your <PERSONAL USE SCRIPT ID> and <SECRET> you need to go here : https://www.reddit.com/prefs/apps and on the bottom of the page click on 'Create another app'
  Then choose a name for your app, select 'script', in redirect uri put https://google.com

It's a fairly simple program, but I'm a newbie and the code is not very clean so you may have trouble to go through it.
The program makes 100 API calls to EDIT 100 messages
  Then 1 API call to check if the EDIT on those 100 messages went through
  Then 100 API calls to remove those 100 messages.
  Which makes it 201 API calls per 100 messages.

Reddit allows you 600 API calls every 10 minutes.
So this program will remove on average 30 messages per minute.

Just use 'python <path to main.py> to run the program
