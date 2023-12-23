import asyncio

#Config dictionary
global config
config = dict()
#Global async lock
async_lock = asyncio.Lock()