import glob
import pandas as pd

path = 'scraper'
files = [file for file in glob.glob('../tours_data/*.csv')]
print(len(files))
li = []
for f in files:
    # read in csv
    temp_df = pd.read_csv(f)
    # append df to list
    li.append(temp_df)


df = pd.concat(li, axis=0)
print(df.shape)
df.head()
