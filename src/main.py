import csv
from random import random
import subprocess
import time
import random
import numpy as np
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import VM_runner
import VM_gui
from datetime import datetime
from threading import Thread


# Main method
def main():
    print()
    try:
        while True:
            # Take the input from the user. Returns true if it is a student.
            if mf_instance.take_Input():
                # Take the student's request and execute it.
                mf_instance.process_Request()
            # Move the .csv files created to their proper place.
            mf_instance.move_CSV_Files()
    except Exception as e:
        print("error happened: " + str(e))
        main()


# MainFunctions class is the class used to store universal functions and help run the main method.
class MainFunctions:
    def __init__(self):
        self.workingId = None
        self.requestedItem = None
        self.is_Admin = False
        self.gambling = False

    # Function to take input from the user and determine if they have admin privileges. If user is an
    # admin, this function returns False, if the user is a student, it returns True. This function
    # also handles all the logic for students being able to gamble for parts.
    def take_Input(self):
        self.gambling = False
        print("taking input now")
        self.workingId = self.take_Id()
        if not self.is_Admin:
            print("taking request now")
            itemToGet = self.take_Request()
            print("got request:" + str(itemToGet))
            if len(str(itemToGet)) > 1 and str(itemToGet)[0] == '/' and str(itemToGet)[1] == '/':
                print("The user wants to gamble")
                self.gambling = True
                itemNum = str(itemToGet)[2]
                if(len(str(itemToGet)) > 3):
                    itemNum+= str(itemToGet)[3]
                self.requestedItem = int(itemNum)
            else:
                print("The user is not a gambler... What a pansie")
                self.requestedItem = itemToGet
            if self.gambling:
                answer = gui.getRequestScreen("You would like to gamble for " + retriever.getStockNameFromId(self.requestedItem) + " for $" + str((retriever.getPrice(self.requestedItem)) / 2) + "? 1 for yes, 0 for no, then press enter.")           
            else:
                answer = gui.getRequestScreen(
                    "You would like a " + retriever.getStockNameFromId(self.requestedItem) + " for $" + str(
                        retriever.getPrice(
                            self.requestedItem)) + "? Press 1 for yes, 0 for no, and then press enter. (remapped from '+')")
            if answer == '1':
                return True
            elif answer == '0':
                return self.take_Input()
            else:
                gui.displayMessage("Please enter a valid input. try again.")
                return self.take_Input()
        else:
            self.admin_Panel()
            self.is_Admin = False
            return False

    # Function which moves all .csv files in /src to /resources/localStorage
    def move_CSV_Files(self):
        print("moving csv files")
        subprocess.call("./bash_scripts/movecsvFiles.sh")
        print("finished moving csv files")

    # Function which stores all logic of the admin panel
    def admin_Panel(self):
        goo = VM_gui.gui()
        try:
            print("Welcome to the Admin panel. Press selection then press enter.")
            print("Press 1 to add balance to a team")
            print("Press 2 to subtract balance from a team")
            print("Press 3 to reduce stock of an item")
            print("Press 4 to add stock to an item")
            print("Press 5 to push current changes to github")
            print("Press 6 to pull data from github")
            print("Press 7 to refresh from origin google sheets")
            print("Press 8 to force push local files to google sheets")
            print("Press 0 to exit Admin Panel")
            selection = gui.adminPanel()
            if int(selection) == 1:
                print(
                    "Select From the teams below. The leftmost number determines the selection")
                teams = retriever.printTeams()
                teamSelection = goo.getRequestScreen(
                    "Select From the teams below. The leftmost number determines the selection\n" + teams, num_rows=28, font_size=15, show_picture=False)
                teamName = retriever.teamFromRow(teamSelection)
                addition = goo.getRequestScreen(
                    "How much money would you like to add?")
                retriever.addMoney(addition, teamName)
            elif int(selection) == 2:
                print(
                    "Select From the teams below. The leftmost number determines the selection")
                teams = retriever.printTeams()
                teamSelection = goo.getRequestScreen(
                    "Select From the teams below. The leftmost number determines the selection\n" + teams, num_rows=28, font_size=15, show_picture=False)
                teamName = retriever.teamFromRow(teamSelection)
                addition = goo.getRequestScreen(
                    "How much money would you like to subtract?")
                retriever.subtractMoney(addition, teamName)
            elif int(selection) == 3:
                item = goo.getRequestScreen(
                    "Which item from the machine would you like to reduce the stock of?")
                amount = goo.getRequestScreen(
                    "How many items should it be reduced by?")
                retriever.subtractStock(item, amount)
            elif int(selection) == 4:
                item = goo.getRequestScreen(
                    "Which item from the machine would you like to increase the stock of?")
                amount = goo.getRequestScreen(
                    "How many items should it be increased by?")
                retriever.addStock(item, amount)
            elif int(selection) == 5:
                self.commit_To_Git()
            elif int(selection) == 6:
                self.pull_From_Git()
            elif int(selection) == 7:
                self.refresh_Local_Files()
            elif int(selection) == 8:
                retriever.force_Update_Sheets()
                self.commit_To_Git()
            elif int(selection) == 9:
                self.forceVend(gui.getRequestScreen(
                    "What Item would you like to force-vend?"))
            elif int(selection) == 0:
                pass
            else:
                goo.displayMessage("Not a correct value. Try again.")
                self.admin_Panel()
        except Exception as e:
            goo.displayMessage("Timeout/Bad input. Closing Admin Panel.")
            return

    # Function which re-instantiates the current retriever instance,
    # therefore pulling data from gsheets
    def refresh_Local_Files(self):
        print("refreshing Local Files")
        global retriever
        # Reset the instance of retriever in order to get data from online again.
        retriever = None
        retriever = DataRetrieval()

    # Function which calls a script to pull data from github.
    def pull_From_Git(self):
        print("starting pull")
        subprocess.call("./bash_scripts/pullDataFromGithub.sh")
        print("finished pulling from github")

    # Function which calls a script to commit and push data to github.
    def commit_To_Git(self):
        # call the script which commits the .csv files
        print("starting commit")
        subprocess.call("./bash_scripts/commitDataToGithub.sh")
        print("finished pushing to github")

    # Function which takes the swipe from the user and returns the id number of the student,
    # or opens the admin panel if the user is an admin
    def take_Id(self):
        print("taking id now")
        self.is_Admin = False
        error = False
        # infinite loop until a valid swipe is made
        while True:
            idnum = gui.getIdCardScreen(error)
            gui.loadingScreen(False)
            retriever.decide_where_to_pull_from()
            gui.closeWindow()
            idnum = vMachine.getId(idnum)
            print("id taken was: " + idnum)
            try:
                # if the user is an admin
                if retriever.checkAdminStatus(idnum):
                    self.is_Admin = True
                    error = False
                    return idnum
                # if the user is a student
                else:
                    error = False
                    return idnum
            except Exception as e:
                # if the user was not found in the dataframe
                print("error was:")
                print(e)
                error = True
                continue

    # Function which takes the input of what item the user wants.
    def take_Request(self):
        first, last = retriever.getName(self.workingId)
        post = "Hello " + first + " " + last + ", Your team, " + retriever.getTeam(self.workingId) + " has $" \
               + str(retriever.getMoney(retriever.getTeam(self.workingId))) + ". "
        return gui.getRequestScreen(
                post + 'Type the number of the item you would like, and then press enter. Or type // and then the item number to gamble!', font_size=25, num_rows=6, num_col=30)

    # Function which checks that the user's request is valid,
    # and executes the request if it is.
    def process_Request(self):
        print("process_request")
        # check what team the user is on
        teamname = retriever.getTeam(self.workingId)
        # check how much money that team has
        money = retriever.getMoney(teamname)
        # check how much money the item the user wants costs
        cost = retriever.getPrice(self.requestedItem)

        if self.gambling:
            cost = cost / 2

        # If the user does not have enough money, or if the item is not in stock.
        if cost > money:
            errormessage = "Your team does not have enough money. You have $" + str(
                money) + " and the requested item costs $" + str(cost) + "."
            print(errormessage)
            gui.displayMessage(errormessage)
        # If the user can afford the item, but the stock is 0
        elif retriever.getStock(self.requestedItem) <= 0:
            errormessage = "There is not any stock of the requested item."
            print(errormessage)
            gui.displayMessage(errormessage, False)
            time.sleep(3)  # wait a few seconds to display the message
            gui.closeWindow()
        # If the user can afford the item, subtract money from their balance and display the vending message
        else:
            if self.gambling:
                random_bit = random.getrandbits(1)
                random_boolean = bool(random_bit)
                if random_boolean:
                    gui.displayMessage("You won your gamble!!! Vending now.", False)
                    time.sleep(3)
                    gui.closeWindow()
                else:
                    gui.displayMessage("You did not win your gamble... sorry",False)
                    time.sleep(3)
                    gui.closeWindow()
                    retriever.add_To_Log("GAMBLE" + str(retriever.getTeam(self.workingId)), str(self.workingId),
                                                str(retriever.getStockNameFromId(
                                                    self.requestedItem)),
                                                str(datetime.now()))
                    return
            retriever.subtractMoney(int(cost), teamname)
            newbalance = "Your balance is now: " + \
                str(retriever.getMoney(teamname))
            gui.displayMessage("Vending item now." + newbalance, True)
            self.execute_Request(self.requestedItem)
            print("Vending item now.")
            retriever.subtractStock(self.requestedItem, 1)
            print(newbalance)
            retriever.push_To_Local()
            # time.sleep(3) this sleep may not be necessary anymore

    # Function which vends the item given the item's id 'itemnum'.
    # Also adds the transaction to the log list.
    def execute_Request(self, itemnum):
        print("executing request.")
        # add to the log
        t1 = Thread(target=retriever.add_To_Log(str(retriever.getTeam(self.workingId)), str(self.workingId),
                                                str(retriever.getStockNameFromId(
                                                    self.requestedItem)),
                                                str(datetime.now())))
        # execute the vending of the item
        t2 = Thread(target=vMachine.vendItem(itemnum))
        t1.start()
        t2.start()
        # If the item did not vend properly, turn the coil again.
        try:
            if not vMachine.ItemVended():
                gui.displayMessage("Item did not vend. Turning coil again.")
                vMachine.vendItem(itemnum)
        except Exception as e:
            gui.displayMessage("problem happened")
            print(e)
            print("Problem turning the coil again.")
        
    
    def forceVend(self,item):
        print("forcing vend")
        gui.displayMessage("Force vending on item #" +
                           str(item) + ". Gsheets will NOT change stock.")
        vMachine.vendItem(item)
        time.sleep(3)
        gui.closeWindow()


# This class handles all necessary data retrieval / data writing for the Vending Machine
class DataRetrieval:
    def __init__(self):
        # Initialize each of the needed variables
        self.online = False
        self.client = None
        self.sheet = None
        self.students = None
        self.teams = None
        self.items = None
        self.log = None
        self.studentsdf = None
        self.teamsdf = None
        self.itemsdf = None
        self.logdf = None

        # Requires internet connection
        try:
            self.decide_where_to_pull_from()
            self.pushLogs()
            self.online = True
        # If the internet connection is not stable
        except Exception as e:
            print(e)
            print("Error when handling files from google sheets. Using local .csv files.")
            self.pull_From_Local()
            self.online = False

    def decide_where_to_pull_from(self):
        self.pull_From_Local()
        print("if statment is: " +
              str(self.logdf.at[len(self.logdf.index)-1, 'transaction_online']))
        if not self.logdf.at[len(self.logdf.index) - 1, 'transaction_online']:
            print(
                "last transaction made was offline, updating sheets from previously made transactions")
            try:
                self.update_sheets_via_logs()
                self.online = True
            except Exception as e:
                print("Couldn't update from logs")
                print(e)
                pass
        else:
            try:
                self.pull_From_Sheets()
            except:
                print("Couldn't pull from sheets")
                pass

    # This function will update the google sheets using data from the local logs, making transactions on the data from google sheets
    def update_sheets_via_logs(self):
        # Start counter at max number of rows
        self.pull_From_Sheets()
        counter = len(self.logdf.index)
        # Loop over all the rows bottom to top until you reach a row that has an online transaction
        while counter > 0 and not self.logdf.at[counter, 'transaction_online']:
            # get the student ID purchaser
            stu_id = self.logdf.at[counter, 'user']
            # get the item purchased
            item_id = self.getIdFromStockName(self.logdf.at[counter, 'part'])
            # charge the student for the item
            self.subtractMoney(self.getPrice(item_id), self.getTeam(stu_id))
            # update the transaction_online variable
            self.logdf.at[counter, 'transaction_online'] = True
            counter = counter - 1

    # This function pulls all data except logs from google sheets into this object's dataframes
    def pull_From_Sheets(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            '../resources/credentials/creds.json', scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open('PythonDatabase')
        self.students = self.sheet.get_worksheet(0)
        self.teams = self.sheet.get_worksheet(1)
        self.items = self.sheet.get_worksheet(2)
        self.studentsdf = pd.DataFrame(self.students.get_all_records())
        self.teamsdf = pd.DataFrame(self.teams.get_all_records())
        self.itemsdf = pd.DataFrame(self.items.get_all_records())
        # Update the local files since it was connected to the internet
        self.push_To_Local()

    # This function allows the caller to add a log record of a purchase to the log.
    # If there is no stable connection to the internet, it will opt to put the log record on the
    # local file "VM_LOG.csv".
    def add_To_Log(self, team, user, part, date):
        # if there is wifi access
        addition = [team, user, part, date, self.online]
        try:
            if self.online:
                self.log.append_row(addition)
                self.logdf.loc[len(self.logdf.index)] = addition
                self.logdf.to_csv("VM_LOG.csv", index=False)
            # if there is no wifi access
            else:
                # go to below block
                raise Exception
        except Exception as e:
            print("went offline.")
            print(e)
            self.online = False
            print("error appending row to google sheets. Using local files")
            # addition = {"team": team, "user": int(user), "part": part, "datetime": date}
            # self.logdf.append(addition, ignore_index=True)
            self.logdf.loc[len(self.logdf.index)] = addition
            self.logdf.to_csv("VM_LOG.csv", index=False)
            print(str(self.logdf))

    # Pull the student's data from local files and fill the necessary dataframes.
    def pull_From_Local(self):
        self.studentsdf = pd.read_csv("../resources/localStorage/VM_USERS.csv")
        self.teamsdf = pd.read_csv("../resources/localStorage/VM_TEAMS.csv")
        self.itemsdf = pd.read_csv("../resources/localStorage/VM_ITEMS.csv")
        self.logdf = pd.read_csv("../resources/localStorage/VM_LOG.csv")

    # Given a student's SMU id, return a bool representing if the student has admin access or not.
    def checkAdminStatus(self, id):
        rownum = self.studentsdf.loc[self.studentsdf["id"] == int(id)].index[0]
        access = self.studentsdf.at[rownum, 'access']
        if access == 'admin':
            return True
        else:
            return False

    # Given a student's SMU id, return the first and last name of the student.
    def getName(self, id):
        row = self.studentsdf.loc[self.studentsdf["id"] == int(id)].index[0]
        first = self.studentsdf.at[row, 'first']
        last = self.studentsdf.at[row, 'last']
        return first, last

    # Given a student's SMU id, return the name of the team which the student is a part of.
    def getTeam(self, id):
        row = self.studentsdf.loc[self.studentsdf["id"] == int(id)].index[0]
        team = self.studentsdf.at[row, 'team']
        print("team name is: " + team)
        return team

    # Given a team's row on the dataframe, return the name of the team.
    def teamFromRow(self, row):
        return self.teamsdf.at[int(row), 'team_name']

    # Print out all the teams stored locally on the dataframe
    def printTeams(self):
        print(self.teamsdf["team_name"])
        return str(self.teamsdf["team_name"])

    # Given a team's name, return the balance of that team
    def getMoney(self, teamname):
        row = self.teamsdf.loc[self.teamsdf["team_name"] == teamname].index[0]
        money = self.teamsdf.at[row, 'bal']
        return money

    # Given the id of an item in the vending machine, return the price of the item.
    def getPrice(self, requesteditem):
        row = self.itemsdf.loc[self.itemsdf["Location"]
                               == int(requesteditem)].index[0]
        return self.itemsdf.at[row, 'Cost']

    # Given the id of an item in the vending machine, return the name of the item.
    def getStockNameFromId(self, id):
        row = self.itemsdf.loc[self.itemsdf["Location"] == int(id)].index[0]
        return self.itemsdf.at[row, 'ItemName']

    # Given the Name of an item in the vending machine, return the id of that item
    def getIdFromStockName(self, name):
        row = self.itemsdf.loc[self.itemsdf['ItemName'] == str(name)].index[0]
        return self.itemsdf.at[row, 'Location']

    # Given the id of an item in the vending machine, return the stock of the item.
    def getStock(self, requesteditem):
        row = self.itemsdf.loc[self.itemsdf["Location"]
                               == int(requesteditem)].index[0]
        return self.itemsdf.at[row, 'Stock']

    # Given the id of an item in the vending machine and a number 'amount', reduce the stock of that item by 'amount'.
    def subtractStock(self, requesteditem, amount):
        rownum = self.itemsdf[self.itemsdf["Location"]
                              == int(requesteditem)].index[0]
        self.itemsdf.at[int(rownum), 'Stock'] = self.itemsdf.at[int(
            rownum), 'Stock'] - int(amount)
        self.update_Files()

    # Given the id of an item in the vending machine and a number 'amount', increase the stock of that item by 'amount'.
    def addStock(self, requesteditem, amount):
        rownum = self.itemsdf[self.itemsdf["Location"]
                              == int(requesteditem)].index[0]
        self.itemsdf.at[int(rownum), 'Stock'] = self.itemsdf.at[int(
            rownum), 'Stock'] + int(amount)
        self.update_Files()

    # Given an int 'amount', and a team name, reduce the balance of that team by 'amount'
    def subtractMoney(self, amount, team):
        rownumber = self.teamsdf[self.teamsdf["team_name"] == team].index[0]
        self.teamsdf.at[int(rownumber), 'bal'] = self.teamsdf.at[int(
            rownumber), 'bal'] - int(amount)
        self.update_Files()

    # Given an int 'amount', and a team name, increase the balance of that team by 'amount'
    def addMoney(self, amount, team):
        rownumber = self.teamsdf[self.teamsdf["team_name"] == team].index[0]
        self.teamsdf.at[int(rownumber), 'bal'] = self.teamsdf.at[int(
            rownumber), 'bal'] + int(amount)
        self.update_Files()

    # Take the current dataframes and pushes them to the local system. (Excludes VM_LOG.csv)
    def push_To_Local(self):
        self.studentsdf.to_csv("VM_USERS.csv", index=False)
        self.teamsdf.to_csv("VM_TEAMS.csv", index=False)
        self.itemsdf.to_csv("VM_ITEMS.csv", index=False)
        subprocess.call("./bash_scripts/movecsvFiles.sh")

    # updates gsheets based on local teamsdf and itemsdf. requires self.sheet to be set
    def update_Files(self):
        try:
            self.teamsdf.to_csv("VM_TEAMS.csv", index=False)
            self.itemsdf.to_csv("VM_ITEMS.csv", index=False)
            self.logdf.to_csv("VM_LOG.csv", index=False)
            sheetName = 'VM_TEAMS'  # set sheet name to put the CSV data into.
            csvFile = 'VM_TEAMS.csv'  # set the filename and path of csv file.
            sh = self.sheet
            self.update_Sheets(sheetName, csvFile, sh)
            sheetName = 'VM_ITEMS'
            csvFile = 'VM_ITEMS.csv'
            self.update_Sheets(sheetName, csvFile, sh)
            sheetName = 'VM_LOG'
            csvFile = 'VM_LOG.csv'
            self.update_Sheets(sheetName, csvFile, sh)
        except:
            print(
                "error updating google sheets from files. pushing to local files instead")
            self.push_To_Local()
            self.online = False

    # Takes the current data in local files and pushes it to the google sheets.
    def force_Update_Sheets(self):
        # get client info and sheet info needed in order to push to gsheets
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            '../resources/credentials/creds.json', scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open('PythonDatabase')
        self.pull_From_Local()
        # call the update_files function
        self.update_Files()
        subprocess.call("./bash_scripts/movecsvFiles.sh")

    # Pushes a given csv file 'csvFile' to the gsheet labeled with 'sheetName'.
    # Requires sh to be the opened PythonDatabase gsheet.
    def update_Sheets(self, sheetName, csvFile, sh):
        sh.values_update(
            sheetName,
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': list(csv.reader(open(csvFile)))}
        )

    # Pulls the logs from the local file and pushes it to the gsheet. requires self.sheet to be set.
    def pushLogs(self):
        self.log = self.sheet.get_worksheet(3)
        self.logdf = pd.read_csv("../resources/localStorage/VM_LOG.csv")
        self.logdf.to_csv("VM_LOG.csv", index=False)
        sheetName = 'VM_LOG'
        csvFile = 'VM_LOG.csv'
        self.update_Sheets(sheetName, csvFile, self.sheet)
        subprocess.call("./bash_scripts/movecsvFiles.sh")


if __name__ == "__main__":
    global vMachine
    vMachine = VM_runner.vender()
    global retriever
    retriever = DataRetrieval()
    global gui
    gui = VM_gui.gui()
    global mf_instance
    mf_instance = MainFunctions()
    print("deciding:")
    retriever.decide_where_to_pull_from()
    try:
        main()
    except Exception as e:
        print('something wrong happened with running main:' + str(e))
        main()
