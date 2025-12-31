from balethon import Client
from balethon.conditions import private
from decouple import config, Csv
import requests

bot = Client(config("BALE_BOT_TOKEN"))
url_send_token = f"{config('SITE_URL')}/api/register/"


@bot.on_message(private)
async def start(message):
    if message.text.startswith("token-"):

        payload = {
            "token": message.text.split("token-")[1].strip(),
            "user_id": message.author.id,
            "first_name": message.author.first_name,
        }

        try:
            response = requests.post(url_send_token, data=payload, timeout=10)
            if response.status_code == 200:
                await message.reply("جهت تکمیل ثبت نام شما لطفا فقط از طریق دکمه پایین صفحه شماره موبایل خود را به اشتراک بگذارید.")
            elif response.status_code == 404:
                await message.reply("توکن معتبر نمی‌باشد. لطفا توکن را مجددا از سایت دریافت کنید.")
            else:
                await message.reply("خطایی به وجود آمد.")
        except Exception as e:
            await message.reply("خطایی به وجود آمد.")
            print(e)



bot.run()