# Program to use Statistics Canada data to calculate number of professors in Canada
# Importing libraries
from io import BytesIO
import numpy as np
import pandas as pd
from urllib.request import urlopen
from zipfile import ZipFile

# Importing data
z = urlopen('https://www150.statcan.gc.ca/n1/tbl/csv/37100077-eng.zip')
myzip = ZipFile(BytesIO(z.read())).extract('37100077.csv')

data = pd.read_csv(myzip)

# A bit of data preparation
# Need to rename a few variables for calcs below
data = data.rename(columns={"Staff functions": "sf", "Number and median": "nm",
"Highest earned degree": "hed"}, errors="raise")

# Also need to create a variable identifying tenured and tenure-track professors
data['tenure'] = 0
data.loc[(data.Rank == 'Assistant professor'),'tenure']= 1
data.loc[(data.Rank == 'Associate professor'),'tenure']= 2
data.loc[(data.Rank == 'Full professor'),'tenure']= 3

# Calculating number of tenure-track or tenured professors in Canada in 2015
year = "2015/2016"
ranks = ["Assistant professor","Associate professor","Full professor"]

numProfs = data[((data.REF_DATE == year) & (data.Sex == "Total sexes") & (data.GEO == "Canada")
& (data.sf == "Total staff function") & (data.nm == "Number of full time teaching staff")
& (data.hed == "PhD (or any equivalent doctoral degree)") & (data.tenure > 0))].pivot_table(index=['REF_DATE'], values=['VALUE'], aggfunc='sum')

numProfs
