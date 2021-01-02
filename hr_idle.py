#!/usr/bin/python3
# Import libraries
from typing import Union


from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import time



# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global curve, ptr, Xm,x, time3,time4
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    #time2=time.perf_counter() #time value at point of income
    value = ser.readline()  # read line (single value) from the serial port
    #if x == True:
    #    time_diff_ms= (time2-time1-(time4-time3))*1000 #difference in milliseconds
    #    time4,time3=0,0
    #else:
    #    time_diff_ms= (time2-time1)*1000
    #time3=time.perf_counter()
    temp: Union[int, bytes]=value[0:len(value) - 2]
    Xm[-1] = float(temp)  # vector containing the instantaneous values
    fo.write(str(Xm[-1])) #write in file 
    #time_diff= "{:.2f}".format(time_diff_ms)
    value_2 = ser.readline()
    temp_2: Union[int, bytes]=value_2[0:len(value_2) - 2]
    #fo.write(' ' + str(time_diff))
    temp_2=int(temp_2)
    fo.write(' ' + str(temp_2))
    fo.write("\n") 
    #print(Xm[-1])
    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 250)  # set x position in the graph to 0
    QtGui.QApplication.processEvents()  # you MUST process the plot now
    #QtGui.QGuiApplication.processEvents()
    #time.sleep(0.001)
    #time4=time.perf_counter()
    #x = True 
    
#file opening
file_name = "ecg1.txt" 
fo = open(file_name, "w")

# Create object serial port
portName = "/dev/cu.usbserial-1430"  # replace this port name by yours!
baudrate = 9600
ser = serial.Serial(portName, baudrate)

### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)
#app: QGuiApplication = QtGui.QGuiApplication([])
####################

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window
p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
curve = p.plot()  # create an empty "plot" (a curve to plot)

windowWidth = 250  # width of the window displaying the curve
Xm = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
ptr = -windowWidth  # set first x position
time1= time.perf_counter() #time at start
x = False

### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot
while True:
        update()
   
    
### END QtApp ####
pg.QtGui.QApplication.exec_()  # you MUST put this at the end
##################
fo.close()
