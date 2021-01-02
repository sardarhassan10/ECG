# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from scipy.signal import find_peaks, detrend
import time
import pywt
import math
import h5py
# set the data points you want
no_rows = 600
start_row = 50


plt.close('all')
t1 = time.process_time()
# data = np.loadtxt('/Users/sardarhassan/Desktop/ecg/ecg1_120.txt',skiprows=50, max_rows=600)
# y = data[:, 0]
# x = data[:, 1]
# x=np.linspace(0,4800,800)

hf = h5py.File('/Users/sardarhassan/Desktop/ecg/ecg.h5', 'r')
print(hf.keys())
n1 = hf.get('ECG')
y = np.array(n1)
n2 = hf.get('Time')
x = np.array(n2)

y = y[start_row:no_rows + start_row]
x = x[start_row:no_rows + start_row]

plt.plot(x, y)
plt.ylabel("Arbitrary Amplitudes")
plt.xlabel("Time/ms")
plt.show()

print (x.shape)
(ca, cd) = pywt.dwt(y, 'db2')

cat = pywt.threshold(ca, np.std(ca) / 1, mode='hard')
cdt = pywt.threshold(cd, np.std(cd) / 1, mode='hard')

y_rec = pywt.idwt(cat, cdt, 'db2')
y = y_rec
# y = detrend(y_rec, type='linear')
plt.plot(x, y)
plt.ylabel("Arbitrary Amplitudes")
plt.xlabel("Time/ms")
plt.show()

# linear spaced vector between 0.5 pi and 1.5 pi
t = np.linspace(0.5 * np.pi, 1.5 * np.pi, 12)
# use sine to approximate QRS feature
qrs_filter = np.sin(t)
print(qrs_filter.shape)
plt.plot(qrs_filter)
plt.ylabel("Amplitude")
plt.xlabel("Points")
plt.show()

# stage 1: compute cross correlation between ecg and qrs filter
similarity = np.correlate(y, qrs_filter, mode="same")
print(similarity.max())
temp2 = similarity.max()
similarity = similarity / 2000
# plt.plot(similarity)
# plt.ylabel("Normalised Similarity")
# plt.xlabel("Bin value")
# plt.show()
# stage 2: find peaks using a threshold
# peaks = temp[similarity > 0.3].index
peaks = np.where(similarity > 0.12)
peaks1 = np.asarray(peaks)
peaks_value = similarity[peaks]
# print(similarity[peaks])
print(peaks1)

# plot detected peaks on graph
plt.plot(similarity)
plt.plot(peaks1, np.repeat(1, peaks1.shape[0]), label="peaks", color="green", marker="o", linestyle="None")
plt.ylabel("Normalised Similarity")
plt.xlabel("Bin value")
plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# initialize output
output = np.empty(0)
peaks2, _ = find_peaks(similarity, height=0.12)
print(peaks2)
peaks2 = np.asarray(peaks2)
plt.plot(similarity)
plt.plot(peaks2, np.repeat(1, peaks2.shape[0]), label="peaks", color="orange", marker="o", linestyle="None")
plt.ylabel("Normalised Similarity")
plt.xlabel("Bin value")
plt.show()

rr = np.diff(x[peaks2])
diff = np.diff(rr)
diff = diff[1:len(diff)]
print(diff)

t2 = time.process_time()
# print((t2-t1)*1000)
print("hr is", 60000 / (np.mean(rr)))
rmssd = np.sqrt(np.mean(np.square(diff)))
print("rmssd in ms is", rmssd)

