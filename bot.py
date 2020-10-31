import discord
import schoolopy
import asyncio
import os
from time import sleep
from json import loads

sc = schoolopy.Schoology(schoolopy.Auth(os.environ.get('SCHOOLOGY_KEY'), os.environ.get('SCHOOLOGY_SECRET')))
sc.limit = 1

def get_updates():
    return(sc.get_group_updates(402741151)[0])


class bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.push_update())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
    async def push_update(self):
        await self.wait_until_ready()
        print('ready')
        channel = self.get_channel(771870347544756275) 
        latest = get_updates()
        x = 0
        while True:
            print('trying')
            sleep(20)
            check_for_diff = get_updates()
            print(latest)
            if check_for_diff['body'] != latest['body']:
                sender = sc.get_user(check_for_diff['uid'])['name_display'].replace(' (Admin)', '')
                body = check_for_diff['body']
                latest = check_for_diff
                await channel.send('**' + sender + '**\n' + body + '**')
            if check_for_diff['body'] == latest['body']:
                x = x + 1
                print('No change, they are equal and even ' + str(x))
            
bot().run(os.environ.get('DISCORD_BOT_SECRET'))
