"""
Extracting Shock Data for Feature Extraction
============================================

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
Raw = pd.read_csv(Raw_signals)

if Terminal:
    print("\n SQI with Clinical Match:")
    print(SQI_C)
    print("\n Raw Signals")
    print(Raw)





