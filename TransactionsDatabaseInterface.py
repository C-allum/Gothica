import sqlite3
import datetime
import numpy as np
from enum import Enum
from CommonDefinitions import sheet as SheetsService, TransactionSheet, liveVersion

import asyncio

#Enum defining valid dezzie moving actions
class DezzieMovingAction(Enum):
    Work = 1        #work command
    Slut = 2        #slut command
    React = 3       #From Dezzie reacts
    Give = 4        #give-money command
    Buy = 5         #When buying items
    Sell = 6        #When selling items
    Add = 7         #LK-command add-money
    Remove = 8      #LK-command remove-money
    Invest = 9      #Investing into community projects
    MessageReward = 10      #Reward for posting in roleplay channels
    RolePay = 11            #Reward for persons with roles, added when working
    StreakReward = 12       #Reward for working without missing a day
    OOCMessageReward = 13   #Reward for posting in non-roleplay channels
    DailyInteraction = 14   #Reward for first interaction per day
    Auction = 15    #When buying a slave


#Initialize the transactions database: connect and create a cursor
def initTransactionsDataBase():
    print("Initializing transactions database...")    
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()

        table = """ CREATE TABLE IF NOT EXISTS Transactions (
                    Date TEXT NOT NULL,
                    Person TEXT NOT NULL,
                    Action TEXT NOT NULL,
                    Amount INT NOT NULL
        );"""

        transactionsCursor.execute(table)
        transactionsConnection.commit()
        transactionsConnection.close()

        print("Transactions Database initialized.\n")
    
    except sqlite3.Error as error:
        print('Error occured while initializing transactions database - ', error)


#Clear the database
def clearTransactions():
    if input("Clear table Transactions? (y/[n])").lower() == 'y':
        try:
            transactionsConnection = sqlite3.connect('CLDTransactions.db')
            transactionsCursor = transactionsConnection.cursor()

            transactionsCursor.execute("DELETE FROM Transactions")
            transactionsConnection.commit()
            transactionsConnection.close()
            
            print("Transactions cleared.\n\n")

        except sqlite3.Error as error:
            print('Error occured while clearing database - ', error)
    else:
        print("Clearing aborted.")


#Add a transaction to the database: Takes a person, an action, an amount and optionally a date in datetime format to write to the Database
def addTransaction(person:str, action:DezzieMovingAction, amount:int, date:datetime.datetime = None):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()

        if date == None:
            date = datetime.datetime.now()

        transactionsCursor.execute(f'''INSERT INTO Transactions VALUES ('{date}', '{person}', '{action.name}', '{amount}')''')
        transactionsConnection.commit()
        transactionsConnection.close()

    except sqlite3.Error as error:
        print('Error occured while adding a transaction to the database - ', error)


#Update a persons name in the Database
def updatePerson(oldPerson:str, newPerson:str):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()

        transactionsCursor.execute(f'''UPDATE Transactions SET person = '{newPerson}' WHERE person = '{oldPerson}' ''')
        transactionsConnection.commit()
        transactionsConnection.close()

    except sqlite3.Error as error:
        print('Error occured while updating a person in the database - ', error)


#Prints contents of the transactions table to the console
def printTransactions(fileName:str = None):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()
        
        data=transactionsCursor.execute('''SELECT * FROM Transactions''').fetchall()

        if fileName is not None:
            with open(fileName, 'w', encoding='utf8') as f:
                for row in data:
                    print(row, file=f)
        else:
            print("Data in table Transactions:")
            for row in data:
                print(row)
            
        transactionsConnection.close()
    except sqlite3.Error as error:
        print('Error occured while printing the database contents - ', error)

#Fetch all accumulated information for one person over a given timeframe
async def playerTransactionsInfo(person:str, timeframe:str = None):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()
        
        #Prints for each person each action plus summed value
        if timeframe is None:
            data = transactionsCursor.execute(f'''SELECT Person, Action, SUM(Amount) FROM Transactions WHERE Person in ('{person}') GROUP BY Person, Action ORDER BY Person, Action''').fetchall()
        else:
            timeframe = "-" + timeframe
            data = transactionsCursor.execute(f'''SELECT Person, Action, SUM(Amount) FROM Transactions WHERE Person in ('{person}') AND date(Date) > date('now', '{timeframe}') GROUP BY Person, Action ORDER BY Person, Action''').fetchall()
            #data=transactionsCursor.execute(f'''SELECT * FROM Transactions WHERE Person in ('{person}') AND date(Date) > date('now', '{timeframe}')''')

        #Print whole database
        #data=transactionsCursor.execute('''SELECT * FROM Transactions''')
            
        transactionsConnection.close()

        return data
    except sqlite3.Error as error:
        print(f'Error occured while printing database contents for - {person}', error)

def transactionSummary(timeframe:str = None):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()
        
        #Prints for each person each action plus summed value
        if timeframe is None:
            data = transactionsCursor.execute(f'''SELECT Person, Action, SUM(Amount) FROM Transactions GROUP BY Person, Action ORDER BY Person, SUM(Amount)''').fetchall()
        else:
            timeframe = "-" + timeframe
            data = transactionsCursor.execute(f'''SELECT Person, Action, SUM(Amount) FROM Transactions WHERE Date > date('now', '{timeframe}') GROUP BY Person, Action ORDER BY Person, SUM(Amount)''').fetchall()
        
        transactionsConnection.close()

        return data

    except sqlite3.Error as error:
        print(f'Error occured getting the transaction summary', error)

def fetchData(timeframe:str = None, summary:bool = False):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()

        if summary is True:
            sqlQuery = "SELECT Person, Action, SUM(Amount) FROM Transactions"
        else:
            sqlQuery = "SELECT * FROM Transactions"
        
        if timeframe is not None:
            timeframe = "-" + timeframe
            sqlQuery += f" WHERE date(Date) > datetime('now', '{timeframe}') "

        if summary is True:
            sqlQuery += f" GROUP BY Person, Action ORDER BY Person, Action"

        data = transactionsCursor.execute(sqlQuery).fetchall()

        return data
    
    except sqlite3.Error as error:
        print('Error occured fetching transaction data - ', error)

#Calculates the average server income over the given timeframe
async def fetchAverageIncome(timeframe:str = "1 Month"):
    transactionsConnection = sqlite3.connect('CLDTransactions.db')
    transactionsCursor = transactionsConnection.cursor()
    
    data = transactionsCursor.execute(f'''SELECT Action, SUM(Amount) FROM Transactions WHERE Date > date('now', '-{timeframe}') GROUP BY Action ORDER BY Action''').fetchall()
    numActivePeople = transactionsCursor.execute(f'''SELECT COUNT(DISTINCT Person) FROM Transactions WHERE Date > date('now', '-{timeframe}')''').fetchall()[0][0]
    
    transactionsConnection.close()
    
    results = f"Active People during the last {timeframe}: {numActivePeople}\n\nTotal Values\n"
    
    for item in data:
        results += str(item[0]) + ": " + str(round((item[1]))) + "\n"
    results += "\nAverage Values\n"
    
    for item in data:
        results += str(item[0]) + ": " + str(round((item[1]) / (numActivePeople), 3)) + "\n"

    return results

#Write data into spreadsheet
#Throws an error if there is no Sheet in the Spreadsheet with the timeframe as name
def dataToSpreadsheet(data, timeframe:str = None):
    try:        
        if timeframe == None:
            timeframe = "Total"

        if liveVersion == 1:
            SheetsService.values().clear(spreadsheetId=TransactionSheet, range=timeframe).execute()
            SheetsService.values().update(spreadsheetId=TransactionSheet, range=timeframe, body=dict(majorDimension='ROWS', values=data), valueInputOption='USER_ENTERED').execute()
            print(f'Wrote transaction data to spreadsheet: {timeframe}')
                    
    except sqlite3.Error as error:
        print('Error occured while printing the database into the spreadsheet - ', error)

#Write a selection of recent transactions to sheets
def automaticTransactionDump():
    dataToSpreadsheet(fetchData('7 Days'), '7 Days')
    dataToSpreadsheet(fetchData('1 Month'), '1 Month')
    dataToSpreadsheet(fetchData('3 Months', summary=True), '3 Months')
    dataToSpreadsheet(fetchData('6 Months', summary=True), '6 Months')
    dataToSpreadsheet(fetchData('1 Year', summary=True), '1 Year')
    dataToSpreadsheet(fetchData(summary=True))

#Given a list, finds and removes outliers. IMPORTANT: ASSUMES NUMBERS ARE IN THIRD ARRAY PLACE
def removeOutliers(data):
    values = sorted([x[2] for x in data])
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    lowerFence_react = q1 - (1.5 * iqr)
    upperFence_react = q3 + (1.5 * iqr)

    outliers = [x for x in data if (x[2] > upperFence_react or x[2] < lowerFence_react)]
    cleanData = [x for x in data if x not in outliers]

    return cleanData, outliers

#Collects all entries where a '#0' identifier is appended to the name and removes those identifiers
def removeZeroIdentifiers():
    transactionsConnection = sqlite3.connect('CLDTransactions.db')
    transactionsCursor = transactionsConnection.cursor()

    data = transactionsCursor.execute(f'''SELECT Person FROM Transactions WHERE Person LIKE '%#0' GROUP BY Person''').fetchall()
    
    listOfNames = [x[0] for x in data]
    listOfNamesWithoutIdentifier = [x[0].split('#')[0] for x in data]

    for (oldName, newName) in zip(listOfNames, listOfNamesWithoutIdentifier):
        updatePerson(oldName, newName)

    transactionsConnection.close()


#--- --- --- TESTING AREA --- --- ---
def testing():
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()
        
        #Collects for each person each action plus summed value
        #data=transactionsCursor.execute('''SELECT Person, Action, SUM(Amount) FROM Transactions GROUP BY Person, Action ORDER BY Person, SUM(Amount)''')

        #Collects for each person action React plus summed value
        actions = ["Work","Slut","React","MessageReward","RolePay","StreakReward"]
        transactionsCursor.execute(f'''SELECT Person, Action, SUM(Amount) FROM Transactions WHERE Action in ({','.join(['?']*len(actions))}) GROUP BY Person, Action ORDER BY Person''', actions)
        data = transactionsCursor.fetchall()

        #Select only values, write to array
        data, outliers = removeOutliers(data)

        #Print whole database
        #data=transactionsCursor.execute('''SELECT * FROM Transactions''')
        
        print('--- Outliers ---')
        for row in sorted(outliers, key=lambda outliers: outliers[2]):
            print(row)

        print('\n--- Data ---')
        for row in sorted(data, key=lambda data: data[2]):
            print(row)
            
        transactionsConnection.close()
    except sqlite3.Error as error:
        print('Error occured while testing - ', error)

def adaptiveQueryTest():
    transactionsConnection = sqlite3.connect('CLDTransactions.db')
    transactionsCursor = transactionsConnection.cursor()

    activePersons = transactionsCursor.execute(f'''SELECT Person FROM Transactions WHERE Date > date('now', '-3 Months') GROUP BY Person, Action ORDER BY Person''').fetchall()

    whatString = "Person, Action, SUM(Amount)"
    sqlQuery = f'''SELECT {whatString} FROM Transactions'''

    #How to add a list of persons to a query
    personsArray = ['tophelin', 'artificer_dragon']
    personsString = "', '".join(personsArray)
    sqlQuery += " \n" + f"WHERE PERSON in ('{personsString}')"

    groupArray = ['Person', 'Action']
    groupString = ', '.join(groupArray)
    sqlQuery += " \n" + f"GROUP BY {groupString}"

    orderArray = ['Person', 'Action']
    orderString = ', '.join(orderArray)
    sqlQuery += " \n" + f"ORDER BY {orderString}"


    data = transactionsCursor.execute(f'''SELECT Person, Action, SUM(Amount) FROM Transactions WHERE Date > date('now', '-3 Months') GROUP BY Person, Action ORDER BY Person, Action''').fetchall()

    print(f"Executing SQL Query:\n{sqlQuery}")

    data = transactionsCursor.execute(f'{sqlQuery}').fetchall()

    transactionsConnection.close()
    
    for row in data:
        print(row)
    

#--- --- --- EXECUTED IF THIS FILE IS RUN --- --- ---
if __name__ == "__main__":
    data = asyncio.run(playerTransactionsInfo('tophelin', '30 Days'))

    for row in data:
        print(row)

    printTransactions("TransactionDump.txt")

