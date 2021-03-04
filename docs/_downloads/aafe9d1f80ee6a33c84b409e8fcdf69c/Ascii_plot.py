"""
Plotting data from an ASCII file (script)
==========================================

Example plot of 'Pleth' and 'ECG1' from an ascii file. 

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Remember to change path
df = pd.read_table(r"D:\FILES\Desktop\Dissertation ICL\OUCRU\01NVa_Dengue\Adults\01NVa-003-2001\Monitor\01NVa-003-2001waves.asc",header=1)

#Visualising Data
df

#Plotting Data
ax = plt.gca()

df[:1000000].plot(kind='line',x='Time',y='ECG1',ax=ax)
df[:1000000].plot(kind='line',x='Time',y='Pleth', color='red', ax=ax)

plt.show()