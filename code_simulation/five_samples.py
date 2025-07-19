
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample

# import the dataset and display 5 samples in the dataset
# update the file name before running the csv file here.
df = pd.read_csv("MaliciousDoH.csv")
df.head(5)

# Distinguish numbers of True and False in sample output.
df.groupby(df.DoH).size()

# remove the features that are unneeded or insignificant
df = df.drop(['SourceIP','DestinationIP','PacketTimeMode','TimeStamp'],1)
df  # displays the expected result

# trauncate samples that contained Na or duplicates
df = df.dropna()
df = df.drop_duplicates()
df

# encode the labels true to binary 1 and false to binary 0
df.DoH = LabelEncoder().fit_transform(df.DoH)

# balance out the sample datasets for DoH verus non-DoH traffic
# in some cases datasets are seemed to perform regular networking activtites than malicious or DoH ones
df_majority = df[df.DoH == 0]
df_minority = df[df.DoH == 1]
df_majority_downsampled = resample(df_majority, replace=False, n_samples=16023, random_state=42)
df = pd.concat([df_majority_downsampled, df_minority])
df.groupby(df.DoH).size()

# Distinguish DoH dataset from the rest of the dataset
X = df.drop('DoH',1)
y = df.DoH

