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

# We could use the below for simplicity but since we are going to be calculating these dataframes for multiple patients,
# then using a csv reader might be more efficient for large scale? Coule we append on axis = 0 multiple dataframes isntead? We would still
# need to read from CSV so that we only carry out once the calculations.

#from plot_SQI_pandas import Signal_SQIs as sqis

#%%
#Loading SQI Data and clinical data

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

'''
We might need to add another function input variable for ID, depending on how we structure
SQI Dataframes i.e. Single or Double

'''
def find_event_time(Clinical,SQIs,event):
    indx_list = []
    date_list = []
    for i in range(len(Clinical['study_no'])):
        #Need to revise this logic, doing this just to get a picture on how to do it
        if Clinical['study_no'][i] == SQIs['study_no'][1] and (Clinical['column'][i] == event and Clinical['result'][i] == 'True' or Clinical['result'][i] == event):
            indx_list.append(i)
            date_list.append(Clinical['date'][i])
    return indx_list, date_list

def find_event_ppg_time(Clinical,SQIs):
    for i in range(len(Clinical['study_no'])):
        #first logical expression needs revisting for multiple SQI Dataframes
        if Clinical['study_no'][i] == SQIs['study_no'][1] and Clinical['column'][i] == 'event_ppg' and Clinical['result'][i] == 'True':
            ppg_start = Clinical['date'][i]
            return ppg_start



ppg_start = find_event_ppg_time(Clinical,SQIs)
print(ppg_start)
indx_list, date_list = find_event_time(Clinical, SQIs, 'event_laboratory')
print(indx_list)
print(date_list)

def calculate_relative_time(ppg_start, date_list):
    relative_event = []
    for i in range(len(date_list)):
        if ppg_start < date_list[i]:
            temp_date_list = datetime.strptime(date_list[i], '%Y-%m-%d %H:%M:%S')
            print(temp_date_list)
            temp_ppg_start = datetime.strptime(ppg_start, '%Y-%m-%d %H:%M:%S')
            print(temp_ppg_start)
            relative_event.append(temp_date_list-temp_ppg_start)
    return relative_event

relative_event = calculate_relative_time(ppg_start, date_list)
print(relative_event)

#%%
Window_position = (relative_event[0].seconds/30) - 10 #(due to the trimming)

#we then match the test to the w of 
print(Window_position)

# %%
## Some thoughts on a single file SQIs (Ignore for now)
'''
ID = [SQIs['study_no'][0]]
for i in range(len(SQIs['study_no']-1)):
    if ID != ID[-1]:
        ID = ID.append(SQIs['study_no'][i+1])
        find_time(Clinical_df, SQIs, 'event_shock', ID)
'''

# %%
