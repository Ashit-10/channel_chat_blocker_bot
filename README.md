## channel_chat_blocker_bot


[![bot logo](https://telegra.ph/file/6e53c92afb8f1784fb86b.jpg)](https://github.com/Ashit-10/channel_chat_blocker_bot)

## Features of this bot
```

- Add me to group , give admin rights (for ban and delete messages atleast)
  and /start to enable/activate me

- /approvechat <tag to message/channel id> :-
   to approve your Channel id (so that you can chat through your channel)

- /disapprovechat <tag to message/channel id> :-
   to ban/disable/block that particular channel id

- /mychannel :- 
   to get your linked channel info

- /list (approved | banned):-
  to get approved/banned list 

- /help :-
   to show this help text

NB:  
  Anonymous admins can't execute bot commands
  You should be an admin or Owner of the group.
```
## Deploy on heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Running bot locally
```
git clone https://github.com/Ashit-10/channel_chat_blocker_bot
```

You need to specify these env variables to run the bot. create a `.env` file.

Add this var 
```
TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"  # your bot's token
```
or replace token in `settings.py`

then `pip -r requirements.txt`

Now start the bot
`python main.py`



## credit

### ``` python-telegram-bot```
