import serial
import time


# Class which handles all hardware use on the vending machine
class vender:
    def __init__(self):
        self.ser = None
        # Try to set up the serial port
        try:
            self.ser = serial.Serial('/dev/ttyUSB0')
            print(self.ser.name)  # check to see the correct port was used
            print("Sleeping to wait for Arduino to reset")
            time.sleep(2)
            print("Sleeping complete")
        # Print exception if the serial port fails.
        except Exception as e:
            print(e)
            print("Something went wrong setting up the arduino")

    # Vend an item given the id of the item.
    def vendItem(self, id):
        try:
            print("input is: " + str(id))
            print("len is: " + str(len(str(id))))
            itemId = str(id)
            if len(itemId) < 2:
                itemId = "0" + itemId
            # Format of output to Arduino is *#*#, where ## is the two-digit representation of the item ID to vend
            toWrite = "*" + itemId[0] + "*" + itemId[1]# + "*"
            print("Vending item " + itemId)
            my_str_as_bytes = str.encode(toWrite)
            self.ser.write(my_str_as_bytes)
        except Exception as e:
            print("item vending failed. Exception: " + str(e))

    # function to be used in main.py in order to retrieve the student's id number from the swipe string
    def getId(self, id):
        # 'E?' is present in all old ids
        if id.count('E?') > 0:
            print("old Id detected")
            return self.getId_Old(id)
        # 'E?' is not present in new ids
        else:
            print("new Id detected")
            return self.getId_New(id)

    # method used to get the id of a student who has an older version of the swipe string
    def getId_Old(self, id):
        pluslocation = id.find('+')
        return id[pluslocation + 1:pluslocation + 9]

    # method used to get the id of a student who has an newer version of the swipe string
    def getId_New(self, id):
        lastdigitloc = len(id) - 1
        return id[lastdigitloc - 8:lastdigitloc]

    # Function used for testing hardware on the vending machine.
    def testing(self):
        swipe = input("Swipe your card.")
        print("string gotten was:" + swipe)
        oldidstyle = "833340041236464821534140?;E?+47876534=GOULD=CHRISTIAN=STUDENT?"  # Christian's ID
        newidstyle = "%4646285093659087259?;46841553612879518=08448510454?"  # Caleb's ID
        oldnewidstyle = "%8337074211684170001166000?;E?+47375514=PUTERBAUGH=ANNA=STUDENT?"  # Anna's ID
        id = swipe
        studentId = self.getId(id)
        print("The result the algorithm returns is: " + str(studentId))

    def testingPing(self):
     ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
     ser.flush()
     time.sleep(1)
     ser.write(b"Begin\n")
     origdist = int(ser.readline().decode('utf-8').rstrip())
     print("orig:" + str(origdist))
      # Take 5000 samples from the arduino
     for i in range(5000):
       ser.write(b"Begin\n")
       x = int(ser.readline().decode('utf-8').rstrip())
       print("x is: " + str(x))
       if(x < origdist-2):
         return True
       time.sleep(0.001)
       return False

    # Detects if an item was vended or not. Uses Universal Serial Bus to detect from a ping sensor the distance across the
    # bottom of the opening in the vending machine
    def ItemVended(self):
      ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
      ser.flush()
      time.sleep(1)
      i = 0
      while i < 500:
         ser.write(b"Begin\n")
         distance = int(ser.readline().decode('utf-8').rstrip())
         print("count: " + str(i) + "dist:" + str(distance))
         if distance < 66:
             return True
         time.sleep(0.001)
         i+=1
      return False


if __name__ == "__main__":
    vendy = vender()
    try:
        if vendy.ItemVended():
            print("the item vended")
        else:
            print("the item did NOT vend")
    except Exception as e:
        print(e)
