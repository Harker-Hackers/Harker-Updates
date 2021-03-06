#!/usr/bin/python3

import logging
import discord
import schoolopy
import asyncio
import os
from time import sleep
from json import loads
from datetime import datetime

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
        await self.change_presence(activity=discord.Game(name='#schoology-updates'))

    async def push_update(self):
        await self.wait_until_ready()
        print('ready')
        channel = self.get_channel(772211342236713001) 
        latest = get_updates()
        spam_channel = self.get_channel(772202956606668810)
        while True:
            try:
                await asyncio.sleep(20)
                check_for_diff = get_updates()
                if check_for_diff['body'] != latest['body']:
                    open('log.txt','w+').write('Update at ' + str(datetime.now().strftime('%H:%M')))
                    sender = sc.get_user(check_for_diff['uid'])['name_display'].replace(' (Admin)', '')
                    body = check_for_diff['body']
                    latest = check_for_diff
                    await channel.send('**' + sender + '**\n' + body)
                await spam_channel.send(str(datetime.now().strftime('%H:%M:%S')))
            except Exception as err:
                print('err')
                open('log.txt','w+').write(str(err))

bot().run(os.environ.get('HARKER_BOT_SECRET'))