#Author: Karol Pawlak
#Description: Banking program - Project S2Y1 - Modular Programming

#importing randint from random needed to generate random 5 didgit account number
from random import randint

#read the file and assign data from the file into lists
def readingFile ():
    bankFile = open("bank.txt", "r") #opening and reading the file
    dataList = bankFile.readlines() #adding each object from the file into a list called fileList
    bankFile.close()
    fileList = []
    for x in dataList: #stripping the objects from /n loaded from the file
        fileList.append(x.strip())
    return fileList

#splitting the lists into three - A/C NUMBERS, A/C BALANCES, CLIENT NAMES
def splitLists(fileList):
    accountNumbers = fileList[0::3] #slicing account numbers only
    accountBalances = convertListToFloat(fileList[1::3]) #slicing balances only and converting to float
    clientNames = fileList[2::3] #slicing names only
    return accountNumbers, accountBalances, clientNames

#function that coverts the list of balances into a float
def convertListToFloat(list):
    newlist = []
    for i in list:
        newitem = float(i)
        newlist.append(newitem)
    return newlist

def startup(text):
    print('{:^45}'.format(text))
    lines = "-" * 45
    print(lines)

def closing():
    lines = "-" * 45
    print(lines)

#main menu of the program
def printMenu ():
    print("Choose one of the following options:")
    print("1. Open an account.")
    print("2. Close an account.")
    print("3. Withdraw money from an account.")
    print("4. Deposit money into an account.")
    print("5. Generate a report for management.")
    print("6. Quit program.")

#validation of user input - in range 1 - 6
def choiceValidation(text):
    validationBoolean = True
    while validationBoolean:
        try:
            userInput = int(input(text))
            if userInput >= 1 and userInput <= 6:
                validationBoolean = False
            else:
                print("ERROR - Please make sure you enter an integer between 1 to 6.")
        except:
            print("ERROR - Please make sure you enter an integer.")
    return userInput

#account number generator
def generateRandomAccountNumber(numberOfDigits, accountsList):
    rangeStart = 10**(numberOfDigits - 1)
    rangeEnd = (10**numberOfDigits) - 1
    #boolean and try except in order to make sure the account number
    #that was generated, does not exist in the list already
    validationBoolean = True
    while validationBoolean:
        try:
            accountNumber = randint(rangeStart, rangeEnd)
            if accountNumber not in accountsList:
                validationBoolean = False
        except:
            break
    return accountNumber

#function that finds index of an item in list
def findIndex(item, list):
    index = list.index(item)
    return index

#function that checks if the account is in the list of account numbers
def checkIfAccountInList(text, accountsList):
    validationBoolean = True
    while validationBoolean:
        try:
            accountNumberInput = input(text)
            if accountNumberInput in accountsList:
                validationBoolean = False
            else:
                print("ERROR - Such account number does not exist.")
        except:
            break
    return accountNumberInput

#function checking and validating the amount entered by the user. taking away from balance
def withdrawFromBalance(text, index, balancesList):
    validationBoolean = True
    while validationBoolean:
        try:
            amount = float(input(text))
            balance = balancesList[index] - amount
            if balance < 0:
                print("ERROR - Insuficient funds.")
            elif amount < 1:
                print("ERROR - You have to enter an amount that is more than 0.")
            else:
                validationBoolean = False
        except:
            print("ERROR - Please make sure you enter an integer.")
    return amount, balance

#function checking and validating the amount entered by the user. adding to balance
def depositToBalance(text, index, balancesList):
    validationBoolean = True
    while validationBoolean:
        try:
            amount = float(input(text))
            balance = balancesList[index] + amount
            if balance < 0:
                print("ERROR - Insuficient funds.")
            elif amount < 1:
                print("ERROR - You have to enter an amount that is more than 0.")
            else:
                validationBoolean = False
        except:
            print("ERROR - Please make sure you enter an integer.")
    return amount, balance


#this function will consist of a while loop that will operate the entire decision process
def choiceSelection (accountsList, balancesList, namesList):
    choiceBoolean = True
    while choiceBoolean:
        printMenu()
        choice = choiceValidation("What would you like to do?>>>")
        if choice == 1:
            openAnAccount(accountsList, balancesList, namesList)
        elif choice == 2:
            closeAnAccount(accountsList, balancesList, namesList)
        elif choice == 3:
            withdrawFromAccount(accountsList, balancesList, namesList)
        elif choice == 4:
            depositToAccount(accountsList, balancesList, namesList)
        elif choice == 5:
            printReport(accountsList, balancesList, namesList)
        else:
            updateFile(accountsList, balancesList, namesList)
            closing()
            print("THANK YOU FOR USING KAROL PAWLAK'S BANKING PROGRAM")
            print("OVERWRITING THE FILE AND QUITTING...")
            closing()

            choiceBoolean = False

def openAnAccount(accountsList, balancesList, namesList):
    startup("OPENING A NEW ACCOUNT")
    name = input("Please enter your first name>>>")
    surname = input("Please enter your surname>>>")
    fullName = name + " " + surname
    balance = 0
    accountNumber = generateRandomAccountNumber(6, accountsList)
    #appending to the lists
    accountsList.append(str(accountNumber))
    balancesList.append(float(balance))
    namesList.append(fullName)
    #
    print("CONGRATULATIONS " + fullName +" - Your account has been created!")
    print("Your account number is: " + str(accountNumber))
    closing()

def closeAnAccount(accountsList, balancesList, namesList):
    startup("CLOSING AN ACCOUNT")
    accountNumber = checkIfAccountInList("Please enter the account number of the account you wish to close:>>>", accountsList)
    accountIndex = findIndex(accountNumber, accountsList)
    #popping the items from the list with the same index as the item entered
    accountsList.pop(accountIndex)
    balancesList.pop(accountIndex)
    namesList.pop(accountIndex)
    #
    name = namesList[accountIndex]
    print("CONGRATULATIONS " + name + " - Your account has been closed.")
    closing()

def withdrawFromAccount(accountsList, balancesList, namesList):
    startup("WITHDRAWING FROM ACCOUNT")
    accountNumber = checkIfAccountInList("Please enter the account number of the account you wish to withdraw from:>>>", accountsList)
    accountIndex = findIndex(accountNumber, accountsList)
    amountToWithdraw, newBalance = withdrawFromBalance("How much would you like to withdraw?>>>", accountIndex, balancesList)
    #changing the old balance with the new
    balancesList[accountIndex] = newBalance
    #
    name = namesList[accountIndex]
    print("CONGRATULATIONS " + name + " - You have withdrawn €" + format(amountToWithdraw, ".2f"))
    print("Your new balance is €" + format(newBalance, ".2f"))
    closing()

def depositToAccount(accountsList, balancesList, namesList):
    startup("DEPOSITING TO ACCOUNT")
    accountNumber = checkIfAccountInList("Please enter the account number of the account you wish to deposit to:>>>", accountsList)
    accountIndex = findIndex(accountNumber, accountsList)
    amountToDeposit, newBalance = depositToBalance("How much would you like to deposit?>>>", accountIndex, balancesList)
    #changing the old balance with the new
    balancesList[accountIndex] = newBalance
    #
    name = namesList[accountIndex]
    print("CONGRATULATIONS " + name + " - You have deposited €" + format(amountToDeposit, ".2f"))
    print("Your new balance is €" + format(newBalance, ".2f"))
    closing()

#function printing the report
def printReport(accountsList, balancesList, namesList):
    startup("PRINTING REPORT FOR MANAGEMENT")
    print('{:20}'.format("ACCOUNT NUMBER") + '{:20}'.format("FULL NAME") + '{:20}'.format("BALANCE"))
    counter = 0
    totalAmountDeposited = 0
    highestBalance = 0
    while counter < len(accountsList):
        print("{:20}".format(str(accountsList[counter])) + "{:20}".format(str(namesList[counter])) + "{:20}".format("€" + str(balancesList[counter])))
        counter += 1
    closing()
    for item in balancesList:
        totalAmountDeposited += item
    print("Total amount deposited in the bank = €" + "{:20}".format(str(totalAmountDeposited)))
    closing()
    highestBalance = max(balancesList)
    highestSaleIndex = balancesList.index(highestBalance)
    print("Details of an account holding the largest amount on deposit in the bank:\n")
    print('{:20}'.format("ACCOUNT NUMBER") + '{:20}'.format("FULL NAME") + '{:20}'.format("BALANCE"))
    print("{:20}".format(str(accountsList[highestSaleIndex])) + "{:20}".format(str(namesList[highestSaleIndex])) + "{:20}".format("€" + str(balancesList[highestSaleIndex])))
    closing()

def updateFile(accountsList, balancesList, namesList):
    #opening the file, but this time writing it new
    bankFile = open("bank.txt", "w")
    counter = 0
    while counter < len(accountsList):
        bankFile.write(str(accountsList[counter]) + "\n")
        bankFile.write(str(balancesList[counter]) + "\n")
        bankFile.write(str(namesList[counter]) + "\n")
        counter += 1
    bankFile.close()

def main():
    accountNumbers, accountBalances, accountNames = splitLists(readingFile())
    startup("BANKING PROGRAM") #opening line of the program - used once only
    choiceSelection(accountNumbers, accountBalances, accountNames)

main()