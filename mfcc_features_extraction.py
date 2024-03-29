# -*- coding: utf-8 -*-
"""MFCC_features_extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wP3jVgpYATKsSLbcFYKb7Hej88YAR11-
"""

#Name: H Kesava Sravan, K Sujan Surya, N Hari Charan, Kavya Balaji
#Roll No.: CB.EN.U4ELC20023, CB.EN.U4ELC20031, CB.EN.U4ELC20041, CB.EN.U4ELC20029
#Objective: To extract features using MFCC algorithm
#Inputs: Audio file
#Outputs: Mel frequency cepstral coefficients

#!pip install librosa
#!pip install xlwt
#!pip install openpyxl

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.style as ms
ms.use('seaborn-muted')
# %matplotlib inline
import librosa
import librosa.display
import IPython.display

#Importing the dataset
from google.colab import files         #To upload files from pc
uploaded = files.upload()
## Load WAV with Librosa
wav_pathname = "noise.wav"
y, sr = librosa.load(wav_pathname)
librosa.display.waveplot(y, sr)
df = pd.DataFrame(y)
df.to_excel('input.xlsx')
print(sr)

IPython.display.Audio(y, rate=sr)

# Let's make and display a mel-scaled power (energy-squared) spectrogram
S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
# Convert to log scale (dB). We'll use the peak power as reference.
log_S = librosa.amplitude_to_db(S)
# Make a new figure
plt.figure(figsize=(12,4))
# Display the spectrogram on a mel scale
# sample rate and hop length parameters are used to render the time axis
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
# Put a descriptive title on the plot
plt.title('mel power spectrogram')
# draw a color bar
plt.colorbar(format='%+02.0f dB')
# Make the figure layout compact
plt.tight_layout()

# Next, we'll extract the first 13 Mel-frequency cepstral coefficients (MFCCs)
mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=13)
# Padding first and second deltas
delta_mfcc  = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
# We'll show each in its own subplot
plt.figure(figsize=(12, 6))

plt.subplot(3,1,1)
librosa.display.specshow(mfcc)
plt.ylabel('MFCC')
plt.colorbar()

plt.subplot(3,1,2)
librosa.display.specshow(delta_mfcc)
plt.ylabel('MFCC-$\Delta$')
plt.colorbar()

plt.subplot(3,1,3)
librosa.display.specshow(delta2_mfcc, sr=sr, x_axis='time')
plt.ylabel('MFCC-$\Delta^2$')
plt.colorbar()

plt.tight_layout()

# Stacking these 3 tables together into one matrix
M = np.vstack([mfcc, delta_mfcc, delta2_mfcc])

df1 = pd.DataFrame(mfcc)
df2 = pd.DataFrame(delta_mfcc)
df3 = pd.DataFrame(delta2_mfcc)
#define list of DataFrames
writer = pd.ExcelWriter('MFCC_Coefficents.xlsx')
# Write each dataframe to a different worksheet.
df1.to_excel(writer, sheet_name='Sheet1')
df2.to_excel(writer, sheet_name='Sheet2')
df3.to_excel(writer, sheet_name='Sheet3')
# Close the Pandas Excel writer and output the Excel file.
writer.close()

## Examining Mel object
print(len(S))
print(len(S[0]))
print(len(S[127]))

## Time test: Load WAV and extract Mel coefficients
import time
start_time = time.time()
y, sr = librosa.load(wav_pathname)
mel_=librosa.feature.mfcc(S=log_S, n_mfcc=13)
stop_time = time.time()
print("Total time computed: ",(stop_time - start_time))