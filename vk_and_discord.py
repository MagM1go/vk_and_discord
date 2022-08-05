import requests

import disnake
from disnake.ext import commands
import vk_api
from vk_api.longpoll import VkLongPoll

VK_TOKEN = ""
DISCORD_TOKEN = "TOKEN"

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())
vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
session = requests.Session()
uploading = vk_api.VkUpload(vk_session)

async def send_message_to_vk(message: str = None, attachments: list = None) -> str:
    vk.messages.send(
        user_id=...,
        message=message if message else ".",
        attachment=', '.join(attachments) if attachments else None,
        random_id=0
    )

@bot.listen('on_ready')
async def on_ready_event():
    print("started")

@bot.listen('on_message')
async def on_message_to_vk(message: disnake.Message):
    if not message.author.bot:
        if len(message.attachments) == 0:
            await send_message_to_vk(message=message.content)
        else:
            for i in message.attachments:
                photo = uploading.photo_messages(photos=session.get(i, stream=True).raw)[0]
                await send_message_to_vk(
                    attachments=[f'photo{photo["owner_id"]}_{photo["id"]}']
                )

bot.run(DISCORD_TOKEN)
