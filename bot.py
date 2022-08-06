import os
import os.path
import glob
from telegram import *
from telegram.ext import *
from urllib.request import urlopen
from settings import *
import time
import json
from datetime import datetime

###########################

def start(update, context):
  user=str(update.message.from_user.id)  
  group=str(update.message.chat_id)
  groupu=f"@{update.message.chat.username}"
  Bchat="-0123456789"
  Bcid="@none"
  if str(update.message.chat.type) == "private":
    update.message.reply_text(f"Hey hello *{update.message.from_user.first_name}* !\ncheck /help for more info\n_Thanks :)_", parse_mode='markdown')
  else:
   try:
     adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
     print(adm)
     if str(adm) == "creator" or str(adm) == "administrator":
         if os.path.isfile(f"{group}_ban_appr_lists.txt") and os.path.isfile(f"{group}_ban_appr_lists.txt"):
            update.message.reply_text("`service is online ...`", parse_mode='markdown')
         else:
          try:
            Lchat=str(context.bot.get_chat(update.message.chat_id).linked_chat_id)
            Lcid=str(context.bot.getChat(Lchat).username)
            Lcid=f"@{Lcid}"
            if not Lchat:
              Lchat="-0123456789"
          except:
               Lchat="-0123456789"
               Lcid="@none"
          dict_grp={
    groupu: {
   "approved_chats": {
     group: groupu,
     Lchat: Lcid     
   },
   "banned_chats": {
    Bchat: Bcid
   }
 }
}
          print(dict_grp)
          with open(f"{group}_ban_appr_lists.txt", 'w+') as f:
              json.dump(dict_grp, f, indent=4, sort_keys=True)
          update.message.reply_text("▶️ *Service has been started !*", parse_mode='markdown')
          try:
             kk=context.bot.getChat(Lchat).username
             print(f"\n\nSTARTED INFO:\ngroup name = @{update.message.chat.username}\nlinked Channel = @{kk}\n\n")
          except:
           try:
             print(f"\n\nSTARTED INFO:\ngroup name = @{update.message.chat.username}\nlinked Channel = None\n\n")
           except:
            pass
   except:
     update.message.reply_text("`Hey! \nI'm can block channel chat messages\nYou can customise me\ncheck /help for more info.`", parse_mode='markdown')
     pass
def help(update, context):
  if str(update.message.chat.type) == "private":
     update.message.reply_text(f"""- Add me to group, give admin rights (ban users and delete messages atleast)
   and `/start` to enable/activate me\n
- `/approvechat` <tag to message/channel username or id> :-
   _to approve your Channel id (so that you can chat through your channel)_\n
- `/disapprovechat` <tag to message/channel id> :-
   _to ban/disable/block that particular channel id_\n
- `/mychannel` :- 
  _ to get your linked channel info_\n
- `/list (approved | banned)`:-
  _to get approved/banned list_ \n
- `/help` :-
   _to show this help text_\n
*NB:  Anonymous admins can't execute bot commands
You should be an admin or Owner of the group*""", 
parse_mode='markdown')
  else:
     update.message.reply_text("Contact me in PM for help.", reply_markup=InlineKeyboardMarkup(
                 [
                   [
                     InlineKeyboardButton(
                     text=f"Click me !",
                     url=f"http://t.me/{context.bot.username}?start"
                      )
                   ]
                 ]
                 ))        

def appr_ban_list(update, context):
  user=str(update.message.from_user.id)
  listc=[]
  num=0
  
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
      if "approved" in update.message.text.split(' '):
        group=str(update.message.chat_id)
        groupu=f"@{update.message.chat.username}"
        with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
        Nlists=obj[f"{groupu}"]['approved_chats']
        for i in Nlists:                                                     
            word=Nlists[i]
            num += 1
            listc.append(f"""{num}) `{i}`\n     *{word}*""")
            listch='\n'.join(listc)
        update.message.reply_text(f"""*List of approved channel chat ID(s)*:-\n{listch}""", parse_mode='MARKDOWN')
      elif "banned" in update.message.text.split(' '):
        group=str(update.message.chat_id)
        groupu=f"@{update.message.chat.username}"
        with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
        Nlists=obj[f"{groupu}"]['banned_chats']
        for i in Nlists:                                                     
            word=Nlists[i]
            num += 1
            listc.append(f"""{num}) `{i}`\n     *{word}*""")
            listch='\n'.join(listc)
        update.message.reply_text(f"""*List of banned channel chat ID(s)*:-\n{listch}""", parse_mode='MARKDOWN')
      else:
         update.message.reply_text("Give correct argument !")
def approve_channel(update, context):
  user=str(update.message.from_user.id)
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
   try:
     print(adm)
     Lcid=None
     group=str(update.message.chat_id)
     groupu=f"@{update.message.chat.username}"
     try:
       Lcid=str(update.message.reply_to_message.sender_chat.id)
       Lchat=str(update.message.reply_to_message.sender_chat.username)
     except:
      msg=str(update.message.text.split(' ')[1])
      if msg.startswith("@"):
       try:
         Lcid=str(context.bot.getChat(update.message.text.split(' ')[1]).id)
         Lcm=str(update.message.text.split(' ')[1]) 
         Lchat=Lcm.replace('@', '')
       except:
          pass
      elif msg.startswith("-100"):
       try:
         Lchat=str(context.bot.getChat(update.message.text.split(' ')[1]).username)
         Lcid=str(update.message.text.split(' ')[1])   
       except:
        pass
      if Lcid:
       try:
           url=(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/unbanChatSenderChat?chat_id={update.message.chat_id}&sender_chat_id={Lcid}")
           with urlopen(url) as f:
               update.message.reply_text("approved !")      
           with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
           obj[f"{groupu}"]['approved_chats'][f"{Lcid}"]=f'''@{Lchat}'''
           print(obj)
           with open(f"{group}_ban_appr_lists.txt", 'w') as f:
                json.dump(obj, f, indent=4, sort_keys=True) 
       except:         
           with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
           obj[f"{groupu}"]['approved_chats'][f"{Lcid}"]=f'''@{Lchat}'''
           print(obj)
           with open(f"{group}_ban_appr_lists.txt", 'w') as f:
                json.dump(obj, f, indent=4, sort_keys=True) 
           update.message.reply_text("added to approved list !")      
      else:
        update.message.reply_text("chat not found !")
   except:
          update.message.reply_text("No arguments given !")
           
def disapprove_channel(update, context):
  user=str(update.message.from_user.id)
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
     group=update.message.chat_id
     groupu=f"@{update.message.chat.username}"
     id="doesnt_exist"
     error_msg="It doesn't seem to be a valid Channel id !" 
     try:
       msg=update.message.text.split(' ')[1]
       if msg.startswith('-100'):
          id=str(update.message.text.split(' ')[1])   
       elif msg.startswith('@'):
          id=str(context.bot.getChat(update.message.text.split(' ')[1]).id)
       elif update.message.reply_to_message:
          id=str(update.message.reply_to_message.sender_chat.id)
     except Exception as e:
         if str(e) == "list index out of range":
          error_msg="No arguments given !"
     if id.startswith('-100'):
      try:
        url=(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/banChatSenderChat?chat_id={update.message.chat_id}&sender_chat_id={id}")
        with urlopen(url) as f:
          update.message.reply_text("banned !")
      except:
        pass
      try:
                with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                     obj=json.load(f)
                sobj=obj[f"{groupu}"]['approved_chats']   
                del obj[f"{groupu}"]['approved_chats'][f"{id}"]
                with open(f"{group}_ban_appr_lists.txt", 'w+') as q:
                  json.dump(obj, q, indent=4, sort_keys=True)
      except:
        pass
     else:
      update.message.reply_text(error_msg)         
def ban_channel_updates(update, context):
 if update.message.sender_chat:
  id=str(update.message.sender_chat.id)
  group=str(update.message.chat_id)
  pp=[]
  pe=[]
  groupu=f"@{update.message.chat.username}"
#  if os.path.isfile(f"{group}_ban_appr_lists.txt"):
  if id.startswith('-100') or id in '777000':
    if str(context.bot.get_chat(update.message.chat_id).linked_chat_id) == id:
       pass
    if str(update.message.chat_id) == id:
       pass
    else:
      try:
        with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
        Nlists=obj[f"{groupu}"]['approved_chats']
        for name in Nlists:
          pe.append(name)
        if id in pe:
           pass
        else:
          try:
            context.bot.delete_message(chat_id=update.message.chat_id,
               message_id=update.message.message_id)
            url=(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/banChatSenderChat?chat_id={update.message.chat_id}&sender_chat_id={update.message.sender_chat.id}")
            with urlopen(url) as f:
                print(f"banned {update.message.sender_chat.id}")
            try:
             with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                 obj=json.load(f)
             Nlists=obj[f"{groupu}"]['banned_chats']
             for name in Nlists:
                pp.append(name)
             if id in pp:
               pass
             else:
                bunned=context.bot.send_message(chat_id=update.message.chat_id, 
                          reply_to_message_id=None,
                parse_mode='markdown',
                text=f"*#banned_channel_chat*\nchannel Id = `{update.message.sender_chat.id}`\nchannel = @{update.message.sender_chat.username}")
                with open(f"{group}_ban_appr_lists.txt", 'r') as f:
                     obj=json.load(f)
                obj[f"{groupu}"]['banned_chats'][f"{id}"]=f'''@{update.message.sender_chat.username}'''
                with open(f"{group}_ban_appr_lists.txt", 'w') as f:
                    json.dump(obj, f, indent=4, sort_keys=True)
            except:
                pass
          except Exception as e:
              print(str(e))
      except:
         pass

def myChannel(update, context):
  user=str(update.message.from_user.id)
  adm=context.bot.getChatMember(chat_id=update.message.chat_id, user_id=user).status
  if adm == "creator" or adm == "administrator":
   try:
      kk=context.bot.get_chat(update.message.chat_id).linked_chat_id
      uname=context.bot.getChat(kk).username
      update.message.reply_text(f"_Linked info:_\n*Channel id* = `{kk}`\n*username* = @{uname}", parse_mode='markdown')
   except:
     update.message.reply_text("Your group doesn't have a channel linked !")
def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(PrefixHandler('/', 'list', appr_ban_list))
    dp.add_handler(PrefixHandler('/', 'approvechat', approve_channel))
    dp.add_handler(PrefixHandler('/', 'mychannel', myChannel))
    dp.add_handler(PrefixHandler('/', 'disapprovechat', disapprove_channel))
    dp.add_handler(MessageHandler(Filters.chat_type.supergroup, ban_channel_updates))
    return dp
