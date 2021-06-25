"""
PPG Pre-processing and SQI Calculations using Pandas on multiple Patients
=========================================================================

Trimming, Filtering, Segmentation and SQI Calculations utilising Pandas on Multiple Patients

"""

# Code Adapted from:
# https://meta00.github.io/vital_sqi/_examples/others/plot_pipeline_02.html
# AND
# https://meta00.github.io/vital_sqi/_examples/others/plot_read_signal.html#sphx-glr-examples-others-plot-read-signal-py

#%%
# Importing Libraries

# Generic
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from datetime import datetime
import glob

# Scipy
from scipy.stats import skew, kurtosis, entropy

 # vitalSQI
from vital_sqi.data.signal_io import PPG_reader
import vital_sqi.highlevel_functions.highlevel as sqi_hl
import vital_sqi.data.segment_split as sqi_sg
from vital_sqi.common.rpeak_detection import PeakDetector
from vital_sqi.preprocess.band_filter import BandpassFilter
import vital_sqi.sqi as sq

filepath_start = r'..\..\..\..\OUCRU\01NVa_Dengue\Adults'
filename_Clinical = r'..\..\..\..\OUCRU\Clinical\v0.0.10\01nva_data_stacked_corrected.csv'
files = os.listdir(filepath_start) # fetching the list of records (currently only 3 for processing simplicity)

#Loading Clinical Data to a Dataframe

Clinical = pd.read_csv(filename_Clinical)

#defining constants
trim_amount = 300
hp_filt_params = (1, 1) #(Hz, order)
lp_filt_params = (20, 4) #(Hz, order)
filter_type =  'butter'
segment_length = 30
sampling_rate = 100

TERMINAL = True

#%%
#Defining Functions
#==================

#find the start of PPG from clinical Data
def find_event_ppg_time(Clinical,Patient):
    row = Clinical[(Clinical.study_no == Patient) & (Clinical.column == 'event_ppg') & (Clinical.result == 'True')]
    return row['date'].values

#======================================================

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

#======================================================

# SQI Functions Definitions

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

'''
MSQ values that are being calculated are too small, maybe peakdetectors need
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

#======================================================

# Function Computing SQIs

def sqi_all(x,raw,filtered,peaks,troughs):
    
    #Computing  all SQIs using the functions above
    
    # Information
    dinfo = {
        'PPG_w_s': x.PPG_Datetime.iloc[0], #timedate window start
        'PPG_w_f': x.PPG_Datetime.iloc[-1], #timedate window finish
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


# %%
#Loop calculating SQIs of multiple records and concatenating results into a single dataframe
#===========================================================================================

'''
Looking through the directories and creating the SQI Dataframe for all patients.
We first calculate each patients SQIs and the carry out the rejection process (latter not yet implementred).
We then concatenate the SQIs along with other descriptors into a single SQI file.
'''

#reading the studies and automatically parsing the files
for i in range(len(files)):
    filepath_end = os.listdir(os.path.join(filepath_start,files[i],r'PPG'))
    filename = os.path.join(filepath_start,files[i],r'PPG',filepath_end[0])
    data = pd.read_csv(filename)
    
    if TERMINAL:
        print(data)
        #print(data.PLETH)
        #print(data.IR_ADC)
        #print(data.TIMESTAMP_MS)
        #print(data.SPO2_PCT)

    signals = data[["PLETH", "IR_ADC"]]

    if TERMINAL:
        # In the future we will be using plotly, for better graphs but due to processing times 
        # that change hasn't been made yet
        plot_range = np.arange(0,1000,1)
        fig, ax = plt.subplots()
        ax.plot(plot_range, signals.iloc[0:1000, 0])
    
    # Setting the indexes for the raw data - adopted from examples
    pd.Timedelta.__str__ = lambda x: x._repr_base('all')
    
    # Include column with index
    signals = signals.reset_index()

    #creating the timedelta index using ms
    signals['timedelta'] = pd.to_timedelta(data.TIMESTAMP_MS, unit='ms')

    #fetching the PPG start date
    PPG_start_date = find_event_ppg_time(Clinical, files[i][-8:])

    #converting to datetime format
    PPG_start_date = datetime.strptime(PPG_start_date[0], '%Y-%m-%d %H:%M:%S')

    #creating the PPG Datetime column by taking the datetime and adding the timedeltas to it for each datapoint
    signals['PPG_Datetime'] = pd.to_datetime(PPG_start_date)
    signals['PPG_Datetime']+= pd.to_timedelta(signals.timedelta)

    # Set the timedelta index (keep numeric index too)
    signals = signals.set_index('timedelta')

    # Rename column to avoid confusion
    signals = signals.rename(columns={'index': 'idx'})

    if TERMINAL:
        print("\n Raw Signals:")
        print(signals)

        #Plotting
        fig, axes = plt.subplots(nrows=2, ncols=1)
        axes = axes.flatten()
        signals.iloc[:,1].plot(ax=axes[0])
        signals.iloc[:,2].plot(ax=axes[1])
    
    # Trimming the first and last 5 minutes

    #Defining the 5 minute offset
    offset = pd.Timedelta(minutes=5)

    #Indexes - adopted from example
    idxs = (signals.index > offset) & \
            (signals.index < signals.index[-1] - offset)

    #Trimming
    signals = signals[idxs]
    
    if TERMINAL:
        print('\n Truncated Signals:')
        print(signals)
    
    
    # RESAMPLE??
    # MISSING DATA INPUT??
    # TAPPERING??

    #Band-pass filtered signals
    signals['PLETH_bpf'] = bpf(signals.iloc[:,1])
    signals['IR_ADC_bpf'] = bpf(signals.iloc[:,2])

    if TERMINAL:
        print('\n Raw and Filtered Signals:')
        print(signals)

        fig, axes = plt.subplots(nrows=2, ncols=1)
        axes = axes.flatten()
        signals['PLETH_bpf'].plot(ax=axes[0])
        signals['IR_ADC_bpf'].plot(ax=axes[1])

    #Calculating peaks and troughs using peakdetector function for both filtered signals
    peak_list_0, trough_list_0 = PeakDetection(signals['PLETH_bpf'])
    peak_list_1, trough_list_1 = PeakDetection(signals['IR_ADC_bpf'])

    # Calculating SQIs for both signals 0 = Pleth and 1 = IR_ADC using both filtered and unfiltered signals
    sqis_0 = signals.groupby(pd.Grouper(freq='30s')).apply(lambda x: sqi_all(x, 'PLETH','PLETH_bpf', peak_list_0, trough_list_0))
    sqis_1 = signals.groupby(pd.Grouper(freq='30s')).apply(lambda x: sqi_all(x, 'IR_ADC','IR_ADC_bpf', peak_list_1, trough_list_1))

    #Displaying the SQIs per signal
    print("SQIs Signal 0 (Pleth):")
    sqis_0
    print(sqis_0)

    print("SQIs Signal 1 (IR_ADC):")
    sqis_1
    print(sqis_1)
    #removing duplicates 
    sqis_1 = sqis_1.drop(['first','last', 'PPG_w_s', 'PPG_w_f'], axis = 1)

    # Add window id to identify point of interest more easily
    sqis_1['w'] = np.arange(sqis_1.shape[0])



    #Final Formatting into a single DataFrame and Saving into a .csv file

    #Merging SQIs of different signals from the same record (Pleth and IR_ADC) 
    Signal_SQIs = sqis_0.merge(sqis_1, on='timedelta', suffixes=('_0', '_1'))

    #Automatically fetching the study_no from the filename and including it in the DataFrame
    Signal_SQIs['study_no'] = files[i][-8:]

    if TERMINAL:
        print('\n Individual SQI Check:')
        print(Signal_SQIs)

    '''

    Discarding process to be added here.

    '''

    #concatenating into a single dataframe for all studies
    if i == 0:
        Complete_SQIs = Signal_SQIs
    else:
        Complete_SQIs = pd.concat([Complete_SQIs, Signal_SQIs])

#Saving to csv format
Complete_SQIs.to_csv(r'..\..\..\..\OUCRU\Outputs\Complete_SQIs.csv')

#%%
# SQI Requirements
#example of the output
img = plt.imread(r'..\..\..\..\MISC\SQI_requirements.png')
plt.title('SQI Requirements')  
plt.imshow(img)