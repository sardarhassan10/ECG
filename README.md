# ECG
Ignore the hr_idle file, it is for rough code testing.
The values folder contains txt and h5 files for ECG data,
with ground truth HR as the file name.
"heart_rate_" file contain Arduino code for ECG monitor. Code taken from Sparkfun AD8232 sensor website.
ECG_Analysis file contains python code for ECG analysis.
PYQT5_ECG file contains code to display ECG data coming from port using PYQT5.
Run Arduino code first, then PYQT5_ECG, and finally ECG_Analysis.
