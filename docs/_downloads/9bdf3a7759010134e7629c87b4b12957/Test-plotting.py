"""
Plotting data from an CSV file (script)
=======================================

Example plot of 'PULSE_BPM' and 'SPO2_PCT' from a CSV file. 

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Remember to Change Path
df = pd.read_csv(r"D:\FILES\Desktop\Dissertation ICL\OUCRU\01NVa_Dengue\Adults\01NVa-003-2001\PPG\01NVa-003-2001 Smartcare.csv")

#visualising Data
df

#Plotting Data
ax = plt.gca()

df[:10000].plot(kind='line',x='TIMESTAMP_MS',y='PULSE_BPM',ax=ax)
df[:10000].plot(kind='line',x='TIMESTAMP_MS',y='SPO2_PCT', color='red', ax=ax)

plt.show()

