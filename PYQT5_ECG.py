import sys
from PyQt5 import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial
import time
from typing import Union
import h5py

file_name = "/Users/sardarhassan/Desktop/ecg1.txt"
fo = open(file_name, "w")
h5_file_name = '/Users/sardarhassan/Desktop/ecg1.h5'
fo_h5 = h5py.File(h5_file_name, 'w')

# create arrays to store values
time_axis = []
ecg_axis = []

# Create object serial port
portName = "/dev/cu.usbserial-1430"  # replace this port name by yours!
baudrate = 9600
ser = serial.Serial(portName, baudrate)


class ecg(QtGui.QWidget):
    def __init__(self):
        super(ecg, self).__init__()
        self.init_ui()
        self.qt_connections()
        self.plotcurve = pg.PlotCurveItem()
        self.plotwidget.addItem(self.plotcurve)
        self.temp = 0

        self.windowWidth = 250  # width of the window displaying the curve
        self.Xm = np.linspace(0, 0, self.windowWidth)  # create array that will contain the relevant time series
        self.ptr = -self.windowWidth  # set first x position
        # self.ptr = 0
        self.xaxis = np.linspace(0, 0, self.windowWidth)
        self.temp5 = np.linspace(0, 0, self.windowWidth)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(10)

    def init_ui(self):
        self.setWindowTitle('ECG Monitor')
        hbox = QtGui.QVBoxLayout()
        self.setLayout(hbox)

        self.plotwidget = pg.PlotWidget()
        hbox.addWidget(self.plotwidget)

        self.startbutton = QtGui.QPushButton("Start")
        self.endbutton = QtGui.QPushButton("End")

        hbox.addWidget(self.startbutton)
        hbox.addWidget(self.endbutton)

        self.setGeometry(10, 10, 1000, 600)
        self.show()

    def qt_connections(self):
        self.startbutton.clicked.connect(self.on_startbutton_clicked)
        self.endbutton.clicked.connect(self.on_endbutton_clicked)

    def moveplot(self):
        self.t += 1
        self.updateplot()

    def updateplot(self):
        if self.temp == 1:
            while self.temp == 1:
                self.Xm[:-1] = self.Xm[1:]  # shift data in the temporal mean 1 sample left
                value = ser.readline()  # read line (single value) from the serial port
                temp: Union[int, bytes] = value[0:len(value) - 2]
                self.Xm[-1] = float(temp)  # vector containing the instantaneous values
                fo.write(str(self.Xm[-1]))  # write in file
                value_2 = ser.readline()
                temp_2: Union[int, bytes] = value_2[0:len(value_2) - 2]
                temp_2 = int(temp_2)
                fo.write(' ' + str(temp_2))
                fo.write("\n")
                # append array to store data in h5 file
                ecg_axis.append(self.Xm[-1])
                time_axis.append(temp_2)

                self.xaxis[:-1] = self.xaxis[1:]
                self.ptr += 1  # update x position for displaying the curve
                self.xaxis[-1] = self.ptr
                if self.xaxis.min() >= 0:
                    self.plotcurve.setData(self.xaxis, self.Xm)
                else:
                    self.plotcurve.setData(self.xaxis, self.temp5)
                self.qt_connections()
                QtGui.QApplication.processEvents()  # you MUST process the plot now

    def on_startbutton_clicked(self):
        self.temp = 1

    def on_endbutton_clicked(self):
        self.temp = 2


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('ECG Monitor')
    ex = ecg()
    sys.exit(app.exec_())
    fo.close()
    fo_h5.create_dataset('ECG', data=ecg_axis, maxshape=(None,))
    fo_h5.create_dataset('Time', data=time_axis, maxshape=(None,))
    fo_h5.close()


if __name__ == '__main__':
    main()
