# GHDBVendingMachine
Hello, welcome to the ENGR 1357 Vending machine application!
Here is the EDITABLE(be careful with it!) link to the database that the Vending machine interfaces with:

[Source of Database](https://docs.google.com/spreadsheets/d/1R_QFsgFUdp9zi6mFOSPCwlzhBSBwfQsvDE9louqXmPg/edit?usp=sharing)

The order of the sheets should be: VM_USERS,VM_TEAMS,VM_ITEMS,VM_LOG

Fun Fact! GHDB originally meant Git-Hub-Data-Based, though it was changed for the better into Google sheets based. 

This means the acronym now stands for:
Gould-Has-Done-Better!

## Table Of Contents
* [Maintenance and Use of the Vending Machine](#maintenance-and-using-the-vending-machine)
* [Getting Google Drive API set up](#getting-google-drive-api-set-up)
* [Starting with a new machine](#starting-a-new-machine)
* [Arduino Sure-Vend](#arduino-sure-vend)
* [Gambling](#gambling)
* [Development of the Machine](#development)

## Maintenance and Using the Vending machine

### Table of Contents
1. [What the Students See](#what-the-students-see)
2. [How to use the Admin Panel](#how-to-use-the-admin-panel)

### What the Students See
- What the students see is a very small UI with only a couple of features.
- First thing that students will be greeted by is a screen asking them to swipe their card. As of the writing of this, the best, most reliable way for them to swipe in is to swipe, mag strip to the right, bottom to top. If they swipe top down, more likely than not, it will not read properly, and then it will ask them to swipe bottom to top.
- Next, they will be asked to select the item that they wish to purchase. If they enter an invalid item number, it will send them back to the swipe screen.
- After selecting a valid item number, then they will press enter and will be greeted with a confimation of their purchase. If they confirm, the item will vend, and their team will be charged.
- Then it will go to the beginning screen.

### How to Use the Admin Panel
The admin panel gives options that may be useful for a faculty member / TA to use. 
After 10 seconds of inactivity, the panel will auto-close for security reasons, so know what you want to select before you swipe.

There are 10 options on the admin panel:
1. Add balance to a team - you can add balance to a team by a specified amount using this
2. Reduce balance of a team - you can reduce the balance of a team by a specified amount.
3. Reduce stock of an item - reduces the stock of an item by a specified amount, and immediately updates the google sheets if possible. Can be useful when force-vendng an item to a student.
4. Increase stock of an item - increases stock of an item by a specified amount, can be useful when re-stocking items.
5. Push current changes to github - used for debugging. Calls a bash script which commits the current team balances and item stock .csv's to github.
6. Pull current changes from github - used for debugging. Calls a bash script with stashes current changes and pulls from github.
7. Refresh from origin google sheets - used to force-update google sheets 
8. Force push local files to google sheets - takes the currently stored .csv files(Items, team balances, and logs) and overwrites the current google sheets. Can be useful when the vending machine has not had internet access for a little while.
9. Force vend - Makes the machine vend an item, and DOES NOT update google sheets. Can be useful for: Inventory, stuck items, etc.
0. Exit - Exits the admin panel and goes back to the ID swipe screen

[Back to the top](#table-of-contents)


## Getting Google Drive API set up
The first thing that needs to be done is getting credentials set up for giving the raspberry pi access to the google sheets.

This portion was excerpted from this tutorial: https://blog.coupler.io/how-to-use-google-sheets-as-database/

### Table Of Contents:
* [Enable The API](#enable-the-api)
* [Create a Service Account](#create-a-service-account)
* [Create a New Key](#create-a-new-key)

### Enable the API
Skip this if you are using the same service account
1. Go to the [Google APIs Console](https://console.developers.google.com/)
2. Click “Select a project” in the top-right corner
![select a project](resources/pictures/one.png)
3. Click the “New Project” option
![new proj. option](resources/pictures/two.png)
4. Give a unique name to your project and click “Create”
![unique name](resources/pictures/three.png)
5. Go to the [API's Dashboard](https://console.cloud.google.com/apis/dashboard)
6. Search for “Google Sheets API” and click on it
![search for api](resources/pictures/four.png)
7. Click “Enable” and wait for the API to be enabled
![enable](resources/pictures/five.png)

### Create a Service Account
Also Skip this if using the same service account
1. When the API is enabled, move to the [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click the “Create credentials” option and select “Service Account”
![create creds](resources/pictures/six.png)
3. Give a name to the service account and click “Create”
![create service acc](resources/pictures/seven.png)
4. Click “Select a role” => “Project” => “Editor”
![select a role](resources/pictures/eight.png)
5. Click “Done”

### Create a new Key
1. In the [Credentials](https://console.cloud.google.com/apis/credentials) page, click on your service account name
![credentials](resources/pictures/nine.png)
2. Go to “Keys”

![go to keys](resources/pictures/ten.png)

3. Select “Add Key” => “Create new key”

![add key](resources/pictures/eleven.png)

4. Leave the option as JSON and click “Create”

![create json](resources/pictures/twelve.png)

5. This action will download a JSON file – rename that file creds.json. This file will hold a lot of sensitive information (Not that big of a deal since we use a dedicated google account for this and this only, unless a student finds it), so make sure not to put it out on the internet publicly anywhere. The file should look something like this:
![rename file](resources/pictures/thirteen.png)
6. put this newly-made creds.json file in resources > credentials in this repo.
7. Find "client_email" in the .json file and copy it. We will use this to give access to the sheets.
8. Now open the google sheets you wish to use, click "Share" and paste the email in there. You may or may not need to click the one option in the dropdown(the option should be named the same as the email) for it to properly share.

[Back to the top](#table-of-contents)

## Starting a New Machine
This is a tutorial on how to get the filesystem structure set up for the vending machine to operate.
firstly, the git repository needs to be set up. To do this, from a fresh terminal, copy and paste these commands:
```
cd Desktop/
git config --global credential.helper store
git clone https://github.com/SMUENGR1357/GHDBVendingMachine.git
```
The terminal will then ask for a username and password. Enter this for these fields: (Note: for those unfamiliar with entering linux passwords in terminal, whatever you type when it asks for password, it will not appear on the screen while you type, so make sure you type it correctly.)
```
Username: engrvm1357@gmail.com
Password: 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
```
Now, you should have a directory on your desktop. We need to set up the script to auto-start on boot. To start, lets give permissions to all the scripts:
Make sure not to miss the trailing "." on the first command!
```
mv ./GHDBVendingMachine/src/bash_scripts/startupScript.sh .
chmod +x ./GHDBVendingMachine/src/bash_scripts/commitDataToGithub.sh
chmod +x ./GHDBVendingMachine/src/bash_scripts/pullDataFromGithub.sh
chmod +x ./GHDBVendingMachine/src/bash_scripts/movecsvFiles.sh
chmod +x ./startupscript.sh
sudo nano /etc/rc.local
```
Scroll down, and just before the exit 0 line, enter the following:
```
./home/pi/Desktop/startupScript.sh
```

Now press ctr+x, press y, and then press enter to exit the nano text editor.
To end, type:
```
sudo reboot
```
And the raspberry pi should reboot and automatically boot into the Vending Machine!

[Back to the top](#table-of-contents)

## Arduino Sure Vend

The Vending machine has been equipped with an arduino-mega and an echo ping sensor at the bottom of the opening which students use to get their items.

The ping sensor and arduino mega are used by the python program to detect when and item drops, and turns the coil a second time if the item did not vend. To preven t many items from dropping if the system fails, the maximum turns allowed is 2, so that if it fails, then the student will just have a lucky day and get 2 items.

The arduino works this way:
* Await a serial signal
* If signal arrives, then take a ping reading
* return the ping reading via the serial bus
* Python will take over all the other logic

The code for this is stored [here](https://github.com/SMUENGR1357/GHDBVendingMachine/blob/main/src/arduino_code/pingthing.ino)

[Back to the top](#table-of-contents)

## Gambling

Students are able to gamble for items. This is how it works

* The student enters "//" and then the item number of what they want ex.) "//02"
* The vending machine will take a random bool, and if it comes out true, then the student will be charged half the price of the item
* If the bool comes out false, then the student will still be charged half the price of the item.
* In essence, this should mean the student gets the item, but there is still a small chance that they come out with nothing.

This feature was just made for a little fun :)

[Back to the top](#table-of-contents)

## Development

The development process began Fall 2021 by [Christian Gould](https://github.com/Gouldilocks)
This was a project made as my first python program. I learned what I could and wrote the entirety of the first workable verision in about a week. Any abnormalities in my Python should be attributed to my inexperience with the programming language.

The main flowchart that the program follows in a nutshell is this:

```
1. Student swipes their card
2. Machine attempts to connect to Google sheets database
3. if failure, pull from current, locally-stored .csv files
4. if success, pull from Google sheets
5. Store data into pandas dataframe
6. ask student to enter the item they want
7. execute the transaction logically, updating the dataframe with correct information
8. execute the request physically, by vending the item by communicating with the arduino uno
9. update local files
10. attempt to update google sheets
11. if success, back to main menu
12. if failure, log that the transaction was made offline and await reconnection to make the merge.
```

The approach to development was in the order shown by the graphic below. The approach attempted to segment the overall project into 4 portions:

* Logical capability - be able to execute all logical functionality of a "vending machine" contained only to a terminal program.
* Hardware capabilty - be able to execute all logical & physical functionality of the vending machine where the terminal is the main user interface
* Minimum working condition - be able to execute all logical, physical, and have the user interface be fully readable and intuitive
* Quality of Life - On top of minimum working condition, make additions that allow for much easier use of the vending machine for faculty / staff.

[Back to the top](#table-of-contents)

![development process](resources/pictures/vmachine.png)
