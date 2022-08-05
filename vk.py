import asyncio
import aiohttp

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

VK_TOKEN = ""

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
headers = {"Authorization": "Bot TOKEN"}

async def channel_messages():
    url = "https://discord.com/api/v10/channels/1004789828396781590/messages"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def longpoll_listen():
    async with aiohttp.ClientSession() as session:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                last_message = await channel_messages()
                if not 'bot' in last_message[-1]["author"].values():
                    if last_message[0]['content'] != event.text:
                        print(last_message[-1]['content'], event.text)
                        async with session.post(
                            'https://discord.com/api/v10/channels/1004789828396781590/messages', 
                            json={'content': event.text}, 
                            headers=headers
                        ) as _:
                            continue

asyncio.run(longpoll_listen())
