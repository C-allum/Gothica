import sqlite3
import datetime
from enum import Enum

#Enum defining valid dezzie moving actions
class DezzieMovingAction(Enum):
    Work = 1    #work command
    Slut = 2    #slut command
    React = 3   #From Dezzie reacts
    Give = 4    #give-money command
    Buy = 5     #When buying items
    Sell = 6    #When selling items
    Add = 7     #LK-command add-money
    Remove = 8  #LK-command remove-money
    Invest = 9  #Investing into community projects


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


#Add a transaction to the database: Takes a person, an action, an amount of dezzies and optionally a list of item details (shopName, itemName, itemAmount) as well as a date in datetime format to write to the Database
def addTransaction(person:str, action:DezzieMovingAction, amountDz:int, itemData:list = None, date:datetime.datetime = None):
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()

        if date == None:
            date = datetime.datetime.now()

        #Is an item supplied in the function call?
        if itemData == None:
            transactionsCursor.execute(f'''INSERT INTO Transactions VALUES ('{date}', '{person}', '{action.name}', '{amountDz}')''')
        else:
            transactionsCursor.execute(f'''INSERT INTO Transactions VALUES ('{date}', '{person}', '{action.name} - {itemData[0]} {itemData[1]} x {itemData[2]}', '{amountDz}')''')

        transactionsConnection.commit()
        transactionsConnection.close()

    except sqlite3.Error as error:
        print('Error occured while adding a transaction to the database - ', error)

#Prints contents of the transactions table to the console
def printTransactions():
    print("Data in table Transactions:")
    try:
        transactionsConnection = sqlite3.connect('CLDTransactions.db')
        transactionsCursor = transactionsConnection.cursor()
        
        data=transactionsCursor.execute('''SELECT * FROM Transactions''')

        for row in data:
            print(row)
            
        transactionsConnection.close()
    except sqlite3.Error as error:
        print('Error occured while printing the database contents - ', error)
