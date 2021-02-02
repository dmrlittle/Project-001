#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:08:33 2021

@author: mrlittle
"""

import asyncio
import time
import aiohttp
import motor.motor_asyncio

async def get_json(queue, session, url, ind):
    async with session.get(url) as response:
        print(f"Fetching from {url}")
        await queue.put([ind, await response.text()])
        
async def dump_json(queue):
    """
        Format in which the data is stored
        { timestamp : data}
    """
    
    global db
    while True:
        item = await queue.get()
        if(item[0] == 0):
            await db.thecocktaildb.insert_one({str(round(time.time())):item[1]})
        else:
            await db.randomuser.insert_one({str(round(time.time())):item[1]})

async def main(sites):
    queue = asyncio.Queue()
    async with aiohttp.ClientSession() as session:
        ttask = asyncio.ensure_future(dump_json(queue))
        tasks = []
        while True:
            for ind, url in enumerate(sites):
                task = asyncio.ensure_future(get_json(queue, session, url, ind))
                tasks.append(task)
            await asyncio.sleep(5)
        await asyncio.gather(*tasks, return_exceptions=True)
        print(await asyncio.gather(ttask, return_exceptions=True))
        
            
        
if __name__ == "__main__":
    evt_loop = asyncio.get_event_loop()
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017, io_loop=evt_loop)
    db = client.sites_db
    sites = [
        "https://www.thecocktaildb.com/api/json/v1/1/random.php",
        "https://randomuser.me/api/",
    ]
    
    evt_loop.run_until_complete(main(sites))