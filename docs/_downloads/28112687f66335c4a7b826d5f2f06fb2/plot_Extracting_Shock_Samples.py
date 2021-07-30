"""
Extracting Shock Data for Feature Extraction (UNFINISHED)
=========================================================

Fetching shock instances (including symptoms that indicate severe dengue) and structuring the data

"""
#%%
## Importing Libraries

# Generic
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import plotly as pl

Terminal = True

SQI_clinical_file = r'..\..\..\..\OUCRU\Outputs\Complete_SQIs_with_Clinical.csv'
Raw_signals = r'..\..\..\..\OUCRU\Outputs\Raw_signals.csv'


#Loading SQI Matched with clinitcal to the Dataframe
SQI_C = pd.read_csv(SQI_clinical_file)
#Raw = pd.read_csv(Raw_signals)

if Terminal:
    print("\n SQI with Clinical Match:")
    print(SQI_C)
    print("\n Raw Signals")
    #print(Raw)


# %%

event = ['event_shock', 'reshock24','shock_admission',\
     'ascites', 'respiratory_distress', 'ventilation_cannula', \
     'ventilation_mechanical', 'ventilation_ncpap', 'bleeding_severe', \
     'cns_abnormal', 'liver_mild', 'pleural_effusion', 'skidney']

event_shock = 'diagnosis_admission'

SQI_C['keep'] = False
for i in range(len(event)):
    event_s = event[i]
    SQI_C_shock = SQI_C[SQI_C[event_s] == True]
    print("\n Total ", event[i], " events:")
    print(SQI_C_shock)
    SQI_C['keep'][SQI_C_shock.index] = True

SQI_C.to_csv(r'..\..\..\..\OUCRU\Outputs\Complete_SQIs_with_Clinical_keep.csv')

    
    
# %%
