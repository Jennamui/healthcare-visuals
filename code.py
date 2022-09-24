#import packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme(style="whitegrid")

#Loading in the csv file
df = pd.read_csv('data/Georgia_COVID-19_Case_Data.csv')
df
len(df)
df.shape

#Describing the variables
df.info()
list(df)
df['COUNTY'].value_counts()

df_counties = df['COUNTY'].value_counts()
df_counties.head(5)

#Transforming Columns
df['DATESTAMP']

##create copy of existing column
df['DATESTAMP_MOD'] = df['DATESTAMP']
print(df['DATESTAMP_MOD'].head(10))
print(df['DATESTAMP_MOD'].dtypes)

df['DATESTAMP_MOD'] = pd.to_datetime(df['DATESTAMP_MOD'])
df['DATESTAMP_MOD'].dtypes

df[['DATESTAMP', 'DATESTAMP_MOD']]

df['DATESTAMP_MOD_DAY'] = df['DATESTAMP_MOD'].dt.date
df['DATESTAMP_MOD_DAY']

df['DATESTAMP_MOD_YEAR'] = df['DATESTAMP_MOD'].dt.year
df['DATESTAMP_MOD_YEAR']

df['DATESTAMP_MOD_MONTH'] = df['DATESTAMP_MOD'].dt.month
df['DATESTAMP_MOD_MONTH']

df['DATESTAMP_MOD_MONTH_YEAR'] = df['DATESTAMP_MOD'].dt.to_period('M')
df['DATESTAMP_MOD_MONTH_YEAR'].sort_values()
df

df['DATESTAMP_MOD_WEEK'] = df['DATESTAMP_MOD'].dt.week
df['DATESTAMP_MOD_WEEK'] 

df['DATESTAMP_MOD_QUARTER'] = df['DATESTAMP_MOD'].dt.to_period('Q')
df['DATESTAMP_MOD_QUARTER'].sort_values()

df['DATESTAMP_MOD_DAY_STRING'] = df['DATESTAMP_MOD_DAY'].astype(str)
df['DATESTAMP_MOD_WEEK_STRING'] = df['DATESTAMP_MOD_WEEK'].astype(str)
df['DATETIME_STRING'] = df['DATESTAMP_MOD_MONTH_YEAR'].astype(str)

#Getting counties for our analysis (Cobb, Dekalb, Fulton, Gwinnett, Hall)
countList = ['COBB','DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countList

selectCounties = df[df['COUNTY'].isin(countList)]
len(selectCounties)

#Getting specific date/time
#df = length ~90,000
#selectCounties = length 2,830
#selectCountyTime = TBD

selectCountyTime = selectCounties
selectCountyTime['DATESTAMP_MOD_MONTH_YEAR']

selectCountyTime_april2020 = selectCountyTime[selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectCountyTime_april2020)

selectCountyTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05') | (selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04') ]
len(selectCountyTime_aprilmay2020)

selectCountyTime_aprilmay2020.head(50)

#Creating the final dataframe/specifc columns-features-attributes
finaldf = selectCountyTime_aprilmay2020[['COUNTY', 'DATESTAMP_MOD', 'DATESTAMP_MOD_DAY', 'DATESTAMP_MOD_DAY_STRING', 'DATETIME_STRING','DATESTAMP_MOD_MONTH_YEAR','C_New', 'C_Cum','H_New', 'H_Cum', 'D_New','D_Cum']]

#Looking at total COVID cases per month
finaldf_dropdups =  finaldf.drop_duplicates(subset = ['COUNTY', 'DATETIME_STRING'], keep= 'last')
finaldf_dropdups

pd.pivot_table(finaldf_dropdups, values = 'C_Cum', index=['COUNTY'], columns =['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)

vis1 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=finaldf_dropdups)

vis2 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue="COUNTY", data=finaldf_dropdups)

plotly1 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color= 'COUNTY', barmode='group')
plotly1.show()

plotly2 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color= 'COUNTY', barmode='stack')
plotly2.show()

#Looking at total COVID cases by day

daily = finaldf
len(daily)
pd.pivot_table(daily, values = 'C_Cum', index=['COUNTY'], columns =['DATESTAMP_MOD_DAY'], aggfunc=np.sum)

startdate = pd.to_datetime("2020-04-26").date()
enddate = pd.to_datetime("2020-05-09").date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (daily['DATESTAMP_MOD_DAY'] <= enddate)
dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']

vis3 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')

vis4 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')

plotly3 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y= 'C_Cum', color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y= 'H_New', color='COUNTY', barmode= 'group')
plotly4.show()

plotly5 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y= 'H_Cum', color='COUNTY', barmode= 'group')
plotly5.show()

plotly6 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y= 'D_New', color='COUNTY', barmode= 'group')
plotly6.show()

plotly7 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y= 'D_Cum', color='COUNTY', barmode= 'group')
plotly7.show()

dailySpecific['newHospandDeath'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int) 

plotly8 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y= 'newHospandDeathCovid', color='COUNTY', title= "Georgia 2020 COVID Data: Total New Hospitalizations, Deaths, and COVID Cases by County", barmode= 'group', labels= {"DATESTAMP_MOD_DAY" : "Time (Month, Day, Year)", "newHospandDeathCovid" : "Total Count" })
plotly8.show()
plotly8.update_layout(xaxis = dict( tickmode = 'linear', type= 'category'))
plotly8.show()
