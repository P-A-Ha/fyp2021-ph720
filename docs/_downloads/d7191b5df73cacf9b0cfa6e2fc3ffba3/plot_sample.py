"""
Plotting PPGs
============================

"""

# Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# Configuration
# --------------------------
filepath = "filepath"

# --------------------------
# Main
# --------------------------
# Read data
#df = pd.read_csv(filepath)

# Create artificial data
noise1 = np.random.normal(0, 0.5, 1000)
noise2 = np.random.normal(1, 0.25, 1000)
timestamp_ms = np.linspace(0, 100000, 1000)
pulse_bpm = np.sin(timestamp_ms) + 80 + noise1
spo2_pct = np.cos(timestamp_ms) + 97 + noise2

# Build DataFrame
data = pd.DataFrame()
data['TIMESTAMP_MS'] = timestamp_ms
data['PULSE_BPM'] = pulse_bpm
data['SPO2_PCT'] = spo2_pct

# Plot
ax = plt.gca()

data.plot(kind='line', x='TIMESTAMP_MS', y='PULSE_BPM', ax=ax)
data.plot(kind='line', x='TIMESTAMP_MS', y='SPO2_PCT', color='red', ax=ax)

# Show
plt.show()