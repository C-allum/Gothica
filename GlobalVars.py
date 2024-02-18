import asyncio

#Config dictionary
global config
config = dict()

#Global async lock
global async_lock
async_lock = asyncio.Lock()

#Global economy data
global economyData
economyData = None
global inventoryData
inventoryData = None

#Item sheet
global itemdatabase
itemdatabase = []