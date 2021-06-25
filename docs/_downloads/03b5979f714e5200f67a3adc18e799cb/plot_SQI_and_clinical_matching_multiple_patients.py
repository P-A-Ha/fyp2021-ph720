"""
Matching SQI Dataframe Window to Clinical Time of "Event" for Multiple Records
==============================================================================
Matching SQI Dataframe Window to Clinical Time of "Event" for Multiple Records

"""

#%%
# Importing Libraries

from datetime import date
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os 

#%%
# Loading SQI Data and clinical data

filename_SQIs = r'..\..\..\..\OUCRU\Outputs\Complete_SQIs.csv'
filename_Clinical = r'..\..\..\..\OUCRU\Clinical\v0.0.10\01nva_data_stacked_corrected.csv'
study_no_path = r'..\..\..\..\OUCRU\01NVa_Dengue\Adults'

#taking a list of records
study_no_list = os.listdir(study_no_path) # Need to take the last 8 characters i.e. study_no_list[i][-8:]

#reading .csv into dataframes
Clinical = pd.read_csv(filename_Clinical)
SQIs = pd.read_csv(filename_SQIs)

TERMINAL = True

#Showing Data
if TERMINAL:
    print("\n Clincial Data:")
    print(Clinical)
    print("\n SQI Data:")
    print(SQIs)

def match_clinical_to_SQIs(Clinical, SQIs, event, study_no_list):
    SQIs[event]=np.nan #forming an empty column for the event 
    print("\n EVENT: ", event)
    #iterating through the study_no
    for i in range(len(study_no_list)):
        print("\n STUDY-NO: ", study_no_list[i])
        #finding the rows for which the following logic is satisfied
        event_row = Clinical[(((Clinical.column == event) & (Clinical.result == 'True')) | (Clinical.result == event)) & (Clinical.study_no == study_no_list[i][-8:])]
        #iterating through the event row for indexing 
        for j in range(len(event_row)):
            valid_SQI_rows = SQIs[(SQIs.PPG_w_s <= event_row.date[event_row.date.index[j]]) & (SQIs.PPG_w_f > event_row.date[event_row.date.index[j]]) & (SQIs.study_no == study_no_list[i][-8:])]
            SQIs[event][valid_SQI_rows.index] = True #Setting the value to True for the window corresponding to an event
            print("\n Valid Event SQIs Index:")
            print(valid_SQI_rows.index) 
    return SQIs

'''
NOTE: 

We previously had functions that fetched ppg start and 
calculated relative times but since we included the PPG Start times
in the SQI file, that is no longer needed.

'''

#Calling the matching function by first defining the event
event_lookup = 'event_laboratory'
SQIs_with_Clinical = match_clinical_to_SQIs(Clinical, SQIs, event_lookup, study_no_list)

#In the second iteration we call the function with the output of the first one, so that we can form 
#multiple columns of events
event_lookup = 'event_shock'
SQIs_with_Clinical = match_clinical_to_SQIs(Clinical, SQIs_with_Clinical, event_lookup, study_no_list)


if TERMINAL:
    print('\n SQIs with Clinical Event Match:')
    print(SQIs_with_Clinical)


#Saving output to CSV
SQIs_with_Clinical.to_csv(r'..\..\..\..\OUCRU\Outputs\Complete_SQIs_with_Clinical.csv')


if TERMINAL:
    #example of the output
    img = plt.imread(r'..\..\..\..\MISC\SQI_Clinical_Image_example_2.png')
    plt.title('Example a Event Alignment with SQIs in Excel')  
    plt.imshow(img)
    img2 = plt.imread(r'..\..\..\..\MISC\SQI_Clinical_Image_example_3.png')
    plt.imshow(img2)


# %%
