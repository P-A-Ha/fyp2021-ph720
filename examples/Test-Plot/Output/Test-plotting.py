#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %%
df = pd.read_csv(r"D:\FILES\Desktop\OUCRU\01NVa_Dengue\Adults\01NVa-003-2001\PPG\01NVa-003-2001 Smartcare.csv")
# %%
#visualising
df
# %%
#plotting
ax = plt.gca()

df[:10000].plot(kind='line',x='TIMESTAMP_MS',y='PULSE_BPM',ax=ax)
df[:10000].plot(kind='line',x='TIMESTAMP_MS',y='SPO2_PCT', color='red', ax=ax)

plt.show()

# %%
