import asyncio

#Config dictionary
config = dict()

#Global async lock
async_lock = asyncio.Lock()

#Global economy data
economyData = None
inventoryData = None

#Item sheet
itemdatabase = []

#Kink sheet
kinkdatabase = []

#Maintenance mode
maintenance_mode = False