import telebot
from faker import Faker
import random
import pyotp
import re
import string
import os

# TOKEN এখন Railway থেকে নিবে (নিরাপদ)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN সেট করো Railway-এ!")

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

locales = ["en_US", "en_IN", "en_GB", "en_CA", "en_AU"]

def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🌍 Fake Name", callback_data="fake_name"),
        telebot.types.InlineKeyboardButton("📧 Temp Mail", callback_data="temp_mail")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🔐 2FA Code", callback_data="2fa"),
        telebot.types.InlineKeyboardButton("🆔 UID Convert", callback_data="uid_convert")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🍪 Cookies to UID", callback_data="cookies_to_uid"),
        telebot.types.InlineKeyboardButton("👨‍💻 Developer Profile", url="https://t.me/Macro69x")
    )
    return markup

# ================== Helper Functions ==================
def extract_c_user(text):
    match = re.search(r'c_user\s*[:=]\s*(\d+)', text, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r'c_user=(\d+)', text)
    if match:
        return match.group(1)
    return None

def extract_uid(text):
    match = re.search(r'profile\.php\?id=(\d+)', text)
    if match:
        return match.group(1)
    match = re.search(r'facebook\.com/([a-zA-Z0-9._-]+)', text)
    if match:
        part = match.group(1)
        return part if part.isdigit() else part
    if text.isdigit() and len(text) > 8:
        return text
    return None

# ================== Start Command ==================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 **MACRO BOT** চালু আছে!\n\nনিচ থেকে অপশন চাপো 👇", 
                 reply_markup=main_menu())

# ================== Callback Handler ==================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "fake_name":
        name = Faker(random.choice(locales)).name()
        bot.edit_message_text(f"""👤 **Fake Name Generated**

`{name}`

✅ এক ক্লিকে কপি করতে উপরের নামে চাপো""", 
                              chat_id, msg_id, reply_markup=main_menu())

    elif call.data == "temp_mail":
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)) + "@1secmail.com"
        bot.edit_message_text(f"""📧 **Temp Mail Ready**

`{email}`

✅ এক ক্লিকে কপি করতে উপরের ইমেইলে চাপো""", 
                              chat_id, msg_id, reply_markup=main_menu())

    elif call.data == "2fa":
        bot.edit_message_text("🔐 **2FA Code**\n\nতোমার সিক্রেট কী পাঠাও (১৬+ অক্ষর)", 
                              chat_id, msg_id, reply_markup=main_menu())

    elif call.data == "uid_convert":
        bot.edit_message_text("🆔 **UID Convert**\n\nFacebook Profile Link পাঠাও:", 
                              chat_id, msg_id, reply_markup=main_menu())

    elif call.data == "cookies_to_uid":
        bot.edit_message_text("🍪 **Cookies to UID**\n\nপুরো cookies স্ট্রিং পেস্ট করো।\n\nসাথে সাথে `c_user` UID বের করে দিবে।", 
                              chat_id, msg_id, reply_markup=main_menu())

# ================== All Messages Handler ==================
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text = message.text.strip()

    c_user = extract_c_user(text)
    if c_user:
        bot.reply_to(message, f"""🍪 **Cookies থেকে UID পাওয়া গেছে**

`{c_user}`

✅ এক ক্লিকে কপি করতে উপরের UID-এ চাপো""")
        return

    uid = extract_uid(text)
    if uid:
        bot.reply_to(message, f"""🆔 **UID Extracted**

`{uid}`

✅ এক ক্লিকে কপি করতে উপরের UID-এ চাপো""")
        return

    cleaned = re.sub(r'[^A-Z2-7]', '', text.upper())
    if len(cleaned) >= 16:
        code = pyotp.TOTP(cleaned).now()
        bot.reply_to(message, f"""🔐 **2FA Code**

📟 কোড: `{code}`

🔑 Secret: `{cleaned}`""")
        return

print("🚀 **FINAL MACRO BOT** চালু হয়েছে — সব অপশন ফিক্সড + সুপার ফাস্ট")
bot.infinity_polling(none_stop=True, interval=0.5, timeout=30)