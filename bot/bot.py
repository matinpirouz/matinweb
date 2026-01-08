from balethon import Client
from balethon.conditions import private
from balethon.objects import (
    ReplyKeyboard,
    ReplyKeyboardButton,
    ReplyKeyboardRemove,
)
from decouple import config, Csv
import requests

bot = Client(config("BALE_BOT_TOKEN"))
url_update_user = f"{config('SITE_URL')}/api/register/"


@bot.on_message(private)
async def start(message):
    if message.text and message.text.startswith("token-"):

        payload = {
            "token": message.text.split("token-")[1].strip(),
            "user_id": message.author.id,
            "first_name": message.author.first_name,
        }

        try:
            response = requests.post(url_update_user, data=payload, timeout=10)
            if response.status_code == 200:
                await message.reply(
                    text="جهت تکمیل ثبت نام شما لطفا فقط از طریق دکمه پایین صفحه شماره موبایل خود را به اشتراک بگذارید.",
                    reply_markup=ReplyKeyboard([ReplyKeyboardButton(text="ثبت شماره موبایل", request_contact=True)])
                )
                
            elif response.status_code == 404:
                await message.reply("توکن معتبر نمی‌باشد. لطفا توکن را مجددا از سایت دریافت کنید.")
            else:
                await message.reply("خطایی به وجود آمد.")
                print(response.text)
        except Exception as e:
            await message.reply("خطایی به وجود آمد.")
            print(e)
            
    elif message.contact:
        if message.contact.user_id == message.author.id:
                
            payload = {
                "user_id": message.author.id,
                "phone_number": message.contact.phone_number,
            }

            try:
                response = requests.post(url_update_user, data=payload, timeout=10)
                if response.status_code == 200:
                    await message.reply(
                        text=f"شماره موبایل {message.contact.phone_number} ثبت شد.\nجهت تایید اطلاعات به متین وب مراجعه نمایید.",
                        reply_markup=ReplyKeyboardRemove()
                    )
                else:
                    await message.reply("خطایی به وجود آمد.")
                    print(response.text)
            except Exception as e:
                await message.reply("خطایی به وجود آمد.")
                print(e)
            
        else:
            await message.reply(
                "شماره موبایل ارسال شده معتبر نیست.\n_ لطفا شماره موبایل خود را فقط از طریق دکمه ارسال نمایید._"
            )



bot.run()