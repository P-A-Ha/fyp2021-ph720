"""
PPG Pre-processing and SQI Calculations using Pandas
====================================================

Trimming, Filtering, Segmentation and SQI Calculations utilising Pandas

"""

# Code Adapted from:
# https://meta00.github.io/vital_sqi/_examples/others/plot_pipeline_02.html
# AND
# https://meta00.github.io/vital_sqi/_examples/others/plot_read_signal.html#sphx-glr-examples-others-plot-read-signal-py

#%%

'''
This file will be used in calculating the SQIs for each patient (and discarding parts of the signal soon).
A loop will be implemented in future iterations for the different patiend files. In general, the file is built
parametrically so that the procedure can be automated.

'''
#%%
# Importing Libraries

# Generic
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime

# Scipy
from scipy.stats import skew, kurtosis, entropy

 # vitalSQI
from vital_sqi.data.signal_io import PPG_reader
import vital_sqi.highlevel_functions.highlevel as sqi_hl
import vital_sqi.data.segment_split as sqi_sg
from vital_sqi.common.rpeak_detection import PeakDetector
from vital_sqi.preprocess.band_filter import BandpassFilter
import vital_sqi.sqi as sq

#%%
# Loading data


# Filepath definition
filepath = r'..\..\..\..\OUCRU\01NVa_Dengue\Adults\01NVa-003-2001\PPG'
filename = r'01NVa-003-2001 Smartcare.csv'
filename_Clinical = r'..\..\..\..\OUCRU\Clinical\v0.0.10\01nva_data_stacked_corrected.csv'



#defining constants
trim_amount = 300
hp_filt_params = (1, 1) #(Hz, order)
lp_filt_params = (20, 4) #(Hz, order)
filter_type =  'butter'
segment_length = 30
sampling_rate = 100

#reading Clinical Data
Clinical = pd.read_csv(filename_Clinical)

#readind PPG data

data = pd.read_csv(os.path.join(filepath, filename))

# data = PPG_reader(os.path.join(filepath, filename), 
#     signal_idx=["PLETH", "IR_ADC"],
#     timestamp_idx=["TIMESTAMP_MS"],
#     info_idx=["SPO2_PCT","PULSE_BPM","PERFUSION_INDEX"], sampling_rate=sampling_rate)



print(data)
print(data.PLETH)
print(data.IR_ADC)
print(data.TIMESTAMP_MS)
print(data.SPO2_PCT)

signals = data[["PLETH", "IR_ADC"]]

plot_range = np.arange(0,1000,1)
fig, ax = plt.subplots()
ax.plot(plot_range, signals.iloc[0:1000, 0])

#%%
#fetching ppg_start time
def find_event_ppg_time(Clinical,Patient):
    row = Clinical[(Clinical.study_no == Patient) & (Clinical.column == 'event_ppg') & (Clinical.result == 'True')]
    return row['date'].values

# %%
# Setting the indexes for the raw data - adopted from examples
pd.Timedelta.__str__ = lambda x: x._repr_base('all')

#Transposing data.signals to set into columns
#signals = pd.DataFrame(data.signals.T)

# Include column with index
signals = signals.reset_index()

signals['timedelta'] = pd.to_timedelta(data.TIMESTAMP_MS, unit='ms')

PPG_start_date = find_event_ppg_time(Clinical, filename.split()[0][-8:])

PPG_start_date = datetime.strptime(PPG_start_date[0], '%Y-%m-%d %H:%M:%S')

signals['PPG_Datetime'] = pd.to_datetime(PPG_start_date)
signals['PPG_Datetime']+= pd.to_timedelta(signals.timedelta)

# Set the timedelta index (keep numeric index too)
signals = signals.set_index('timedelta')

# Rename column to avoid confusion
signals = signals.rename(columns={'index': 'idx'})

print("Raw Signals:")
print(signals)

#Plotting
fig, axes = plt.subplots(nrows=2, ncols=1)
axes = axes.flatten()
signals.iloc[:,1].plot(ax=axes[0])
signals.iloc[:,2].plot(ax=axes[1])

# %%
# Trimming the first and last 5 minutes

#Defining the 5 minute offset
offset = pd.Timedelta(minutes=5)

#Indexes - adopted from example
idxs = (signals.index > offset) & \
        (signals.index < signals.index[-1] - offset)

#Trimming
signals = signals[idxs]

print(signals)


# %%

# RESAMPLE??
# MISSING DATA INPUT??
# TAPPERING??

#%%
# Band-pass filtering

'''
Band-pass filtering can be adjusted, maybe use a lower low-pass
cutoff frequency @15-17Hz

'''
#Band pass filtering function
def bpf(signal):
    hp_filt_params = (1, 1) #(Cutoff Hz, order)
    lp_filt_params = (20, 4) #( Cutoff Hz, order)
    sampling_rate = 100
    filter = BandpassFilter(band_type='butter', fs=sampling_rate)
    filtered_signal = filter.signal_highpass_filter(signal, cutoff=hp_filt_params[0], order=hp_filt_params[1])
    filtered_signal = filter.signal_lowpass_filter(filtered_signal, cutoff=lp_filt_params[0], order=lp_filt_params[1])
    return filtered_signal

#Band-pass filtered signals
signals['PLETH_bpf'] = bpf(signals.iloc[:,1])
signals['IR_ADC_bpf'] = bpf(signals.iloc[:,2])

print('Raw and Filtered Signals:')
print(signals)

fig, axes = plt.subplots(nrows=2, ncols=1)
axes = axes.flatten()
signals['PLETH_bpf'].plot(ax=axes[0])
signals['IR_ADC_bpf'].plot(ax=axes[1])


# %%
# SQI Functions Definition and Peak Detection

def PeakDetection(x):
    detector = PeakDetector()
    peaks, troughs = detector.ppg_detector(x, 7) #6 and 7 work the best
    return peaks, troughs

#Defining SQI Functions

def snr(x):
    #Signal to noise ratio
    #needs raw signal
    return np.mean(sq.standard_sqi.signal_to_noise_sqi(x))

def zcr(x):
    #Zero Crossing Rate
    #Needs filtered signal
    return 0.5 * np.mean(np.abs(np.diff(np.sign(x))))

def mcr(x):
    #Mean Crossing Rate
    #needs raw signal
    return zcr(x - np.mean(x))

def perfusion(x,y):
    return (np.max(y) - np.min(y)) / np.abs(np.mean(x)) * 100

def correlogram(x):
    #Correlogram
    #Needs filtered signal
    return sq.rpeaks_sqi.correlogram_sqi(x)

#Calculating peaks and troughs using peakdetector function for both filtered signals
peak_list_0, trough_list_0 = PeakDetection(signals['PLETH_bpf'])
peak_list_1, trough_list_1 = PeakDetection(signals['IR_ADC_bpf'])

'''
MSW values that are being calculated are too small, maybe peakdetectors need
to be revisited?
'''
def msq(x,peaks):
    #Dynamic Time Warping
    #Requires Filtered Signal and peaks
     # Return
     return sq.standard_sqi.msq_sqi(x, peaks_1=peaks, peak_detect2=6)

'''
Below function is outputting an error, needs revisiting
'''
# def dtw(x,troughs):
#     #Dynamic Time Warping
#     #Requires Filtered Signal and troughs and template selection 0-3 (0-2 for PPG)
#     # Per beat
#     dtw_list = sq.standard_sqi.per_beat_sqi(sqi_func=sq.dtw_sqi, troughs=troughs, signal=x, taper=True, template_type=1)
#     # Return mean and standard deviation
#     return [np.mean(dtw_list), np.std(dtw_list)]

# %%
# Function Computing SQIs

def sqi_all(x,raw,filtered,peaks,troughs):
    
    #Computing  all SQIs using the functions above
    
    # Information
    dinfo = {
        'PPG_w_s': x.PPG_Datetime.iloc[0],
        'PPG_w_f': x.PPG_Datetime.iloc[-1],
        'first': x.idx.iloc[0],
        'last': x.idx.iloc[-1],
        'skew': skew(x[raw]),
        'entropy': entropy(x[raw]),
        'kurtosis': kurtosis(x[raw]),
        'snr': snr(x[raw]),
        'mcr': mcr(x[raw]),
        'zcr': zcr(x[filtered]),
        'msq': msq(x[filtered],peaks),
        'perfusion': perfusion(x[raw], x[filtered]),
        'correlogram': correlogram(x[filtered]),
        #'dtw': dtw(x[filtered],troughs)
    }
    '''
    When using dtw an empty signal error is presented that
    needs fixing, not sure why it does that
    '''
    # Return
    return pd.Series(dinfo)

#%%
# Calculating SQIs for both signals 0 = Pleth and 1 = IR_ADC

sqis_0 = signals.groupby(pd.Grouper(freq='30s')).apply(lambda x: sqi_all(x, 'PLETH','PLETH_bpf', peak_list_0, trough_list_0))
sqis_1 = signals.groupby(pd.Grouper(freq='30s')).apply(lambda x: sqi_all(x, 'IR_ADC','IR_ADC_bpf', peak_list_1, trough_list_1))

#Displaying the SQIs per signal
print("SQIs Signal 0 (Pleth):")
sqis_0
print(sqis_0)

print("SQIs Signal 1 (IR_ADC):")
sqis_1
print(sqis_1)
sqis_1 = sqis_1.drop(['first','last', 'PPG_w_s', 'PPG_w_f'], axis = 1)


# Add window id to identify point of shock more easily
sqis_1['w'] = np.arange(sqis_1.shape[0])


#%%
# Final Formatting into a single DataFrame and Saving into a .csv file

#Merging SQIs of different signals from the same record (Pleth and IR_ADC) 
Signal_SQIs = sqis_0.merge(sqis_1, on='timedelta', suffixes=('_0', '_1'))

#Automatically fetching the study_no from the filename and including it in the DataFrame
Signal_SQIs['study_no'] = filename.split()[0][-8:]
print(Signal_SQIs)

# Saving the SQIs to a CSV file
Signal_SQIs.to_csv(r'..\..\..\..\OUCRU\Outputs\SQI.csv')


#%%

'''
#Running Some Abstract Checks to Verify Results etc.

print(perfusion(signals[0][0:3000], signals['PLETH_bpf'][0:3000]))

'''

#%%
'''
Discarding Process to be implemented after quality check.
'''
