import pandas as pd

# Load small samples (faster)
logon = pd.read_csv("data/raw/logon.csv", nrows=1000)
file = pd.read_csv("data/raw/file.csv", nrows=1000)
device = pd.read_csv("data/raw/device.csv", nrows=1000)

print("\n--- LOGON ---")
print(logon.head())
print(logon.columns)

print("\n--- FILE ---")
print(file.head())
print(file.columns)

print("\n--- DEVICE ---")
print(device.head())
print(device.columns)