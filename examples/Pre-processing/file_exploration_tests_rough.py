from typing import Counter
import pandas as pd
import os
from datetime import datetime


filepath = r"D:\FILES\Desktop\Dissertation ICL\OUCRU\01NVa_Dengue\Adults\01NVa-003-2009\PPG"
files = os.listdir(filepath)
first = os.path.join(filepath, files[0])
#second = os.path.join(filepath, files[1])

f = pd.read_csv(first)
#s = pd.read_csv(second)

print(f)
#print(s['COUNTER'])

#print(s['COUNTER'].iloc[0] - f['COUNTER'].iloc[-1])
#print(files[0])
#test = files[0][:-13]
#test = test.replace('T','')
#print(test)
#datetime_conversion_check = datetime.strptime(test, '%Y%m%d%H%M%S')
#print(datetime_conversion_check)