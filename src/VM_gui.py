import time
from typing import Sized

import PySimpleGUI as sg
import main
import VM_runner


class gui:
    def __init__(self):
        self.currwindow = None

    def getIdCardScreen(self, error=False, autoclose=True):
        if error:
            textbox = 'That was not a valid swipe. Please try again. (Maybe try swiping bottom up?)'
        else:
            textbox = 'Welcome to the ENGR 1357 Vending Machine. Please start by swiping your ID!'

        sg.theme('Black')
        layout = [[sg.Image(r'../resources/pictures/mustang.png')],
                  [sg.Text(textbox, size=(23, 5), font=("Helvetica", 35), )],
                  [sg.Input('', enable_events=True, key='-INPUT-', do_not_clear=True)],
                  ]

        # Create the Window
        self.currwindow = sg.Window('Vending Machine', layout, no_titlebar=False, location=(0, 0), size=(2000, 2000),
                                    keep_on_top=False, resizable=True).Finalize()
        self.currwindow.Maximize()
        # Event Loop to process "events" and get the "values" of the inputs
        seenEquals = False
        while True:
            returnMe = None
            event, values = self.currwindow.read()
            if event in (None, 'Exit'):  # if user closes window or clicks cancel
                break
            print('You entered in the textbox:')
            print(values['-INPUT-'])  # get the content of multiline via its unique key

            currString = str(values['-INPUT-'])
            if currString.endswith('.'):
                print("ends with character")
                self.currwindow['-INPUT-'].update(value=currString[0:len(currString) - 2])
            if currString.endswith('='):
                seenEquals = True
            if len(values['-INPUT-']) > 7 and seenEquals and currString.endswith('?'):
                print('valid input detected')
                print("input detected was: " + values['-INPUT-'])
                returnMe = values['-INPUT-']
                break
            if event == 'Submit':
                print('user hit submit button')
        if autoclose:
            self.currwindow.close()
        return returnMe

    def getRequestScreen(self, text, autoclose=True, num_rows=5, font_size=35, show_picture=True, num_col=23):
        print(sg.__version__)
        sg.theme("Black")
        if show_picture:
            layout = [[sg.Image(r'../resources/pictures/mustang.png')],
                      [sg.Text(text, size=(num_col, num_rows), font=("Helvetica", font_size))],
                      [sg.Input('', enable_events=True, key='-INPUT-', )],
                      [sg.Button('Submit', visible=False, bind_return_key=True)]
                      ]
        else:
            layout = [
                      [sg.Text(text, size=(num_col, num_rows), font=("Helvetica", font_size))],
                      [sg.Input('', enable_events=True, key='-INPUT-', )],
                      [sg.Button('Submit', visible=False, bind_return_key=True)]
                      ]
        # Create the Window
        self.currwindow = sg.Window('Vending Machine', layout, location=(0, 0), size=(2000, 2000),
                                    resizable=True, keep_on_top=False, no_titlebar=False).Finalize()
        self.currwindow.Maximize()
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            returnMe = None
            event, values = self.currwindow.read()
            if event in (None, 'Exit'):  # if user closes window or clicks cancel
                break
            print('You entered in the textbox:')
            print(values['-INPUT-'])  # get the content of multiline via its unique key
            string_so_far = values['-INPUT-']
            if string_so_far.endswith('.'):
                print("ends with character")
                self.currwindow['-INPUT-'].update(value=string_so_far[0:len(string_so_far) - 2])
            if event == 'Submit':
                print('User hit the submit button')
                print("input detected was: " + values['-INPUT-'])
                returnMe = str(values['-INPUT-'])
                break
            elif string_so_far.endswith('+'):
                print('User pressed +')
                returnMe = string_so_far[0:len(string_so_far) - 1]
                print('Input recieved: ' + returnMe)
                break
        if autoclose:
            self.currwindow.close()
        return returnMe

    def loadingScreen(self, autoclose=True):
        sg.theme('Black')
        layout = [[sg.Text("Loading...", size=(20, 1), font=("Helvetica", 80))],
                  [sg.Image(r'../resources/pictures/itsoncanvas.png')]
                  ]

        # Create the Window
        self.currwindow = sg.Window('Vending Machine', layout, no_titlebar=False, location=(0, 0), resizable=True,
                                    keep_on_top=False, size=(2000, 2000)).Finalize()
        self.currwindow.Maximize()
        self.currwindow.bring_to_front()
        # Event Loop to process "events" and get the "values" of the inputs
        if autoclose:
            self.currwindow.close()

    def displayMessage(self, message, autoclose=True):
        sg.theme('Black')
        layout = [[sg.Text(message, size=(16, 5), font=("Helvetica", 45))]]

        # Create the Window
        self.currwindow = sg.Window('Vending Machine', layout, no_titlebar=False, location=(0, 0),
                                    keep_on_top=False, resizable=True, size=(2000,2000)).Finalize()
        self.currwindow.Maximize()
        self.currwindow.bring_to_front()
        time.sleep(3)
        # Event Loop to process "events" and get the "values" of the inputs
        if autoclose:
            self.currwindow.close()

    def closeWindow(self):
        self.currwindow.close()

    def adminPanel(self):
        text = [
            "Welcome to the Admin panel. Press selection then press enter.",
            "Press 1 to add balance to a team",
            "Press 2 to subtract balance from a team",
            "Press 3 to reduce stock of an item",
            "Press 4 to add stock to an item",
            "Press 5 to push current changes to github",
            "Press 6 to pull data from github",
            "Press 7 to refresh from origin google sheets",
            "Press 8 to force push local files to google sheets",
            "Press 9 to force vend an item",
            "Press 0 to exit Admin Panel"
        ]
        print(sg.__version__)
        sg.theme("Black")
        layout = [
                  [sg.Text(text[0], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[1], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[2], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[3], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[4], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[5], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[6], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[7], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[8], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[9], size=(60, 1), font=("Helvetica", 15))],
                  [sg.Text(text[10], size=(60,1), font=("Helvetica", 15))],
                  [sg.Input('', enable_events=True, key='-INPUT-', )],
                  [sg.Button('Submit', visible=False, bind_return_key=True)]
                  ]

        # Create the Window
        self.currwindow = sg.Window('Vending Machine', layout, location=(0, 0), size=(2000, 2000),
                                    resizable=True, keep_on_top=False, no_titlebar=False,auto_close=True,auto_close_duration=10).Finalize()
        self.currwindow.Maximize()
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            returnMe = None
            event, values = self.currwindow.read()
            if event in (None, 'Exit'):  # if user closes window or clicks cancel
                break
            print('You entered in the textbox:')
            print(values['-INPUT-'])  # get the content of multiline via its unique key
            string_so_far = values['-INPUT-']
            if string_so_far.endswith('.'):
                print("ends with character")
                self.currwindow['-INPUT-'].update(value=string_so_far[0:len(string_so_far) - 2])
            if event == 'Submit':
                print('User hit the submit button')
                print("input detected was: " + values['-INPUT-'])
                returnMe = values['-INPUT-']
                break
            elif string_so_far.endswith('+'):
                print('User pressed +')
                returnMe = string_so_far[0:len(string_so_far) - 1]
                print('Input recieved: ' + returnMe)
                break

        self.currwindow.close()
        return returnMe


if __name__ == "__main__":
    pubgui = gui()
    pubgui.adminPanel()
    time.sleep(3)
