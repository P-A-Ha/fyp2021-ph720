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
study_no_list = os.listdir(study_no_path) # Need to take the last 8 characters i.e. study_no_list[i][-8:]

#reading .csv into dataframes
Clinical = pd.read_csv(filename_Clinical)
SQIs = pd.read_csv(filename_SQIs)

TERMINAL = False

#Showing Data
if TERMINAL:
    print(Clinical)
    print(SQIs)

def match_clinical_to_SQIs(Clinical, SQIs, event, study_no_list):
    SQIs[event]=np.nan #forming an empty column for the event 
    for i in range(len(study_no_list)):
        #finding the rows for which the following logic is satisfied
        event_row = Clinical[(((Clinical.column == event) & (Clinical.result == 'True')) | (Clinical.result == event)) & (Clinical.study_no == study_no_list[i][-8:])]
        #print(event_row)
        #for j in range(len(event_row)):
        #    valid_SQI_rows = SQIs[SQIs.PPG_w_s < event_row[j].date < SQIs.PPG_w_f]
        #    print(valid_SQI_rows)
        
            

            

    return event_row

'''

We previously had functions that fetched ppg start and 
calculated relative times but since we included the PPG Start times
in the SQI file, that is no longer needed.

'''

event_lookup = 'event_laboratory'

SQIs_with_Clinical = match_clinical_to_SQIs(Clinical, SQIs, event_lookup, study_no_list)

print(SQIs_with_Clinical)

#SQIs_with_Clinical.to_csv(r'..\..\..\..\OUCRU\Outputs\Complete_SQIs_with_Clinical.csv')


if TERMINAL:
    img = plt.imread(r'..\..\..\..\MISC\SQI_Clinical_Image_example.png')
    plt.title('Example a Event Alignment with SQIs in Excel')  
    plt.imshow(img)




# %%
