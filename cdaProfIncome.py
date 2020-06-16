# Key script for calculating average professor income in Canada
# Import necessary libraries
from io import BytesIO
import numpy as np
import pandas as pd
from urllib.request import urlopen
from zipfile import ZipFile

# Get "Number and salaries of full-time teaching staff at Canadian universities"
z = urlopen('https://www150.statcan.gc.ca/n1/tbl/csv/37100108-eng.zip')
myzip = ZipFile(BytesIO(z.read())).extract('37100108.csv')

data = pd.read_csv(myzip)
print(len(data))

# Creating indices to identify universities and those with medical schools
data["uniIndex"] = data["Institution"].str.find("Uni", 0) 
data["inclMedIndex"] = data["Institution"].str.find("Including", 0) 
data["exclMedIndex"] = data["Institution"].str.find("Excluding", 0) 

data['university'] = np.where(data['uniIndex'] >=0, 1,0)
data['inclMed'] = np.where(data['inclMedIndex'] >=0, 1,0)
data['exclMed'] = np.where(data['exclMedIndex'] >=0, 1,0)

# Calculating job weighted average for 2015/2016
year = "2015/2016"
ranks = ["Assistant professor","Associate professor","Full professor"]

ranksDict = {"Assistant professor":'AsstProf',"Associate professor":'AssocProf',"Full professor":'FullProf'}

academicPay = data.Institution.unique()
academicPay = pd.DataFrame(academicPay)
academicPay = academicPay.rename(columns={0: 'Institution'})

for i in ranks:
  tempSal = data[((data.Rank == i))
  & (data.inclMed != 1) & (data.REF_DATE == year) & (data.Statistics == "Average")
  ].pivot_table(index=['Institution'], values=['VALUE'], aggfunc='sum')
  academicPay = pd.merge(academicPay, tempSal, on='Institution')
  academicPay = academicPay.rename(columns={'VALUE': '{}Sal'.format(ranksDict[i])})

  tempNum = data[((data.Rank == i))
  & (data.inclMed != 1) & (data.REF_DATE == year) & (data.Statistics == "Total teaching staff")
  ].pivot_table(index=['Institution'], values=['VALUE'], aggfunc='sum')
  academicPay = pd.merge(academicPay, tempNum, on='Institution')
  academicPay = academicPay.rename(columns={'VALUE': '{}Num'.format(ranksDict[i])})


academicPay['totNum'] = academicPay['AsstProfNum'] + academicPay['AssocProfNum'] + academicPay['FullProfNum']
academicPay['sumProduct'] = (academicPay['AsstProfNum'] * academicPay['AsstProfSal'] + academicPay['AssocProfNum']
 * academicPay['AssocProfSal'] + academicPay['FullProfNum'] * academicPay['FullProfSal']) 
academicPay

numerator = academicPay['sumProduct'].sum()
denominator = academicPay['totNum'].sum()

avgProfSalary = numerator/denominator
print(avgProfSalary)
