import os, re, threading

class sensors(threading.Thread):
    global number
    def __init__(self, sensortype, numb):
        global number
        threading.Thread.__init__(self)
        self.sensortype = sensortype
        number = numb + 1
        
    def run(self):
        print("Thread "+ self.sensortype +" startetd")
        print(number)
        
    def status(self):
        return "alive"