"""
Matching SQI Dataframe Window to Clinical Time of Shock
====================================================
Matching SQI Dataframe Window to Clinical Time of Shock

"""
#%%
# Importing Libraries

from datetime import date
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# We could use the below for simplicity but since we are going to be calculating these dataframes for multiple patients,
# then using a csv reader might be more efficient for large scale? Coule we append on axis = 0 multiple dataframes isntead? We would still
# need to read from CSV so that we only carry out once the calculations.

#from plot_SQI_pandas import Signal_SQIs as sqis

#%%
# Loading SQI Data and clinical data

'''
With some string manipulation and a loop we will be able to apply the following pipeline automatically,
depends on how we structure our SQIs i.e. separate dataframes or one large dataframe?
For now let's do it for a single file.

'''
filename_SQIs = r'..\..\..\..\OUCRU\01NVa_Dengue\Adults\01NVa-003-2001\SQI.csv'
filename_Clinical = r'..\..\..\..\OUCRU\Clinical\v0.0.10\01nva_data_stacked_corrected.csv'


#reading .csv into dataframes
Clinical = pd.read_csv(filename_Clinical)
SQIs = pd.read_csv(filename_SQIs)

#Showing Data
print(Clinical)
print(SQIs)

#%%
# Main Functions fetching event time, ppg start time and the relative time
'''
We might need to add another function input variable for ID, depending on how we structure
SQI Dataframes i.e. Single or Double

'''

#Function that fetches the time of a pre-specified event into a list for multiple occurences
def find_event_time(Clinical,SQIs,event):
    indx_list = []
    date_list = []
    for i in range(len(Clinical['study_no'])):
        #Need to revise this logic, doing this just to get a picture on how to do it
        if Clinical['study_no'][i] == SQIs['study_no'][1] and (Clinical['column'][i] == event and Clinical['result'][i] == 'True' or Clinical['result'][i] == event):
            indx_list.append(i)
            date_list.append(Clinical['date'][i])
    return indx_list, date_list

#Calcuating the time of ppg_start
def find_event_ppg_time(Clinical,SQIs):
    for i in range(len(Clinical['study_no'])):
        #first logical expression needs revisting for multiple SQI Dataframes, event_ppg seemed accurate when crosschecking with raw data
        if Clinical['study_no'][i] == SQIs['study_no'][1] and Clinical['column'][i] == 'event_ppg' and Clinical['result'][i] == 'True':
            ppg_start = Clinical['date'][i]
            return ppg_start

#Calculating the relative time i.e. time of event - time of start
def calculate_relative_time(ppg_start, date_list):
    relative_event = []
    for i in range(len(date_list)):
        if ppg_start < date_list[i]: #Makins sure that event is after start of PPG Record
            temp_date_list = datetime.strptime(date_list[i], '%Y-%m-%d %H:%M:%S') #converting str to datetime
            print('Temporary Date List (converted to datetime):')
            print(temp_date_list)
            temp_ppg_start = datetime.strptime(ppg_start, '%Y-%m-%d %H:%M:%S') #converting str to datetime
            print('Temporary PPG Start (converted to datetime):')
            print(temp_ppg_start)
            relative_event.append(temp_date_list-temp_ppg_start) #List of events with relative times
    return relative_event

#Defining the event we are interested in (this one was used as an example as it was the only one that could be used for this specified patient)
event_lookup = 'event_laboratory'

ppg_start = find_event_ppg_time(Clinical,SQIs)
print('PPG Start Time:')
print(ppg_start)
indx_list, date_list = find_event_time(Clinical, SQIs, event_lookup)
print('Event Indexes List:')
print(indx_list)
print('Event Datetime List:')
print(date_list)

relative_event = calculate_relative_time(ppg_start, date_list)
print('Relative Event List:')
print(relative_event)



#%%
# Using the relative time we can calculate the window and then match the event to the SQI window

#The following was used during debugging
#SQIs = SQIs.drop(['Event'], axis = 1)

#We divide by 30 to find the number of windows, -10 for the 5 minute trimming and -1 for the indexing
Window_position = int((relative_event[0].seconds/30) - 10 - 1) #(due to the trimming and indexing of w starting from 0)

#The below is done for the sake of the example as we cannot find an event within the PPG record for this patient (other than Dengue Shock which has no time)
#And we are subtractinf 2513 to be able to easily observe the effect of the actions that follow 
Window_position = Window_position - 2503
print(Window_position)

#%%
# We then match the event to the specific window using indexing and the "w" column constructed earlier.
if SQIs['w'][Window_position]:
    SQIs['Event'] = np.nan #filling up with nans to form the column
    SQIs['Event'][Window_position] = event_lookup #replacing the nan with the event on the specified cell
#The raise below is not really needed since if it is out of range another ValueError will be raised
else:
    raise ValueError('Window not found') #just in case not such window exists

print(SQIs)

#%%
# Save to CSV File

SQIs.to_csv(r'..\..\..\..\OUCRU\01NVa_Dengue\Adults\01NVa-003-2001\SQI_and_clinicals.csv')

#%%
# Allignment Example

img = plt.imread(r'..\..\..\..\MISC\SQI_Clinical_Image_example.png')
plt.title('Example a Event Alignment with SQIs in Excel')
plt.imshow(img)
# %%
# Some thoughts on a single file SQIs (Ignore for now)
'''
ID = [SQIs['study_no'][0]]
for i in range(len(SQIs['study_no']-1)):
    if ID != ID[-1]:
        ID = ID.append(SQIs['study_no'][i+1])
        find_time(Clinical_df, SQIs, 'event_shock', ID)
'''
