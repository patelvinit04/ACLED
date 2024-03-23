import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import solara
import seaborn as sns
from matplotlib import cm
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def get_country(text):
    if ',' in text:
        country = text.split(',')[-1].strip()
        return country
    else:
        return text.strip()

sns.set_theme()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


'''
df = pd.read_csv("Africa_Data.csv")

#Listing all the columns
#print(df.columns)

#Listing unique values in each column
#for column in df.columns:
   #unique_values = df[column].unique()
    #print(f"Unique values in column '{column}': {unique_values}")



df['ACTOR1'] = df['ACTOR1'].astype(str)
df['ASSOC_ACTOR_1'] = df['ASSOC_ACTOR_1'].astype(str)
df['ASSOC_ACTOR_2'] = df['ASSOC_ACTOR_2'].astype(str)
df['ACTOR2'] = df['ACTOR2'].astype(str)
df['NOTES'] = df['NOTES'].astype(str)

#Include Wagner/Russia 
import pandas as pd

words = ['Wagner', 'Russia', 'Russian', "Wagner's", "Russia's", "Wagners"]
columns_to_check = ['ACTOR1', 'ASSOC_ACTOR_1','ASSOC_ACTOR_2', 'ACTOR2', 'NOTES']
dfs = pd.DataFrame()

for word in words:
    for column in columns_to_check:
        filtered_rows = df[df[column].str.contains(fr'{word}', regex=True, case=False)]
        dfs = pd.concat([dfs, filtered_rows])

#dfs.reset_index(drop=True, inplace=True)

#print(len(df))
#print(len(dfs))

#print(dfs.columns)

#exporting the file
#dfs.to_csv('Africa_Wagner.csv', index = False)



ACLED = pd.read_csv("Africa_Wagner.csv")
GDELT = pd.read_csv("GDELTWagnerApril18.csv")
cameo = pd.read_csv("cameo.csv")
GDELT['DISORDER_TYPE'] = None
GDELT['EVENT_TYPE'] = None
GDELT['SUB_EVENT_TYPE'] = None
GDELT['INFO'] = None
indices = 0

for index, row in GDELT.iterrows():
    num = str(row['EventCode'])
    for index2, row2 in cameo.iterrows():
        num2 = str(row2['Number'])
        if (num == num2):
            GDELT.loc[index, 'DISORDER_TYPE'] = row2['DISORDER_TYPE']
            GDELT.loc[index, 'EVENT_TYPE'] = row2['EVENT_TYPE']
            GDELT.loc[index, 'SUB_EVENT_TYPE'] = row2['SUB_EVENT_TYPE']
            GDELT.loc[index, 'INFO'] = row2['MAKE PUBLIC STATEMENT']
            break

#Convert GDELT dates to match ACLED
GDELT['Day'] = GDELT['Day'].astype(str)
for index, row in GDELT.iterrows():
    day_str = str(row['Day'])
    year = int(day_str[:4])
    month = int(day_str[4:6])
    day = int(day_str[6:])
    date_obj = datetime(year, month, day)
    GDELT.loc[index, 'Day']= date_obj.strftime("%d-%B-%Y")


for index, row in GDELT.iterrows():
    check = True
    day_str = str(row['Day'])
    lat = int(row['ActionGeo_Lat'])
    long = int(row['ActionGeo_Long'])
    for index2, row2 in ACLED.iterrows():
        day_str2 = str(row2['EVENT_DATE'])
        lat2 = int(row2['LATITUDE'])
        long2 = int(row2['LONGITUDE'])
        if (day_str2 == day_str) and ((abs(lat2/5) - lat2) < lat < (abs(lat2/5) + lat2)) and ((abs(long2/5) + long2) < long < (abs(long2/5 + long2))):
            check = False
            break
    if check:
        new_row = pd.DataFrame(np.nan, index = [0], columns = ACLED.columns)
        new_row['EVENT_ID_CNTY'] = 'GDELT'
        new_row['EVENT_DATE'] = day_str
        new_row['YEAR'] = day_str[-4:]
        new_row['DISORDER_TYPE'] = row['DISORDER_TYPE']
        new_row['EVENT_TYPE'] = row['EVENT_TYPE']
        new_row['SUB_EVENT_TYPE'] = row['SUB_EVENT_TYPE']
        new_row['ACTOR1'] = 'Wagner Group'
        new_row['ASSOC_ACTOR_1'] = row['Actor1Name']
        new_row['ACTOR2'] = row['Actor2Name']
        new_row['INTER2'] = row['EventCode']
        country = str(row['ActionGeo_Fullname'])
        country = get_country(country)
        new_row['COUNTRY'] = country
        new_row['LATITUDE'] = row['ActionGeo_Lat']
        new_row['LONGITUDE'] = row['ActionGeo_Long']
        new_row['SOURCE'] = row['SOURCEURL']
        new_row['NOTES'] = row['INFO']
        ACLED = pd.concat([new_row, ACLED]).reset_index(drop = True)

ACLED.to_csv('Final.csv', index = False)



'''
df = pd.read_csv("Final.csv")

#Stacked bar chart
countries = (
    df[~df['COUNTRY'].isin(['Mali', 'Central African Republic'])]
    .groupby(['COUNTRY', 'EVENT_TYPE'])
    .size()
    .unstack(fill_value=0)
)

fig, ax = plt.subplots(figsize=(25, 6))

# Create stacked bar chart
countries.plot(kind='barh', stacked=True, ax=ax)
ax.set_title('Number of Events by Disorder Type and Country')
ax.set_xlabel('Number of Events')
ax.set_ylabel('Country')
plt.legend(title='Disorder Type', loc='lower right')
plt.tight_layout()
plt.show()
plt.close()



'''
#Creating columns
# Convert EVENT_DATE to datetime format
df['EVENT_DATE2'] = pd.to_datetime(df['EVENT_DATE'], format='%d-%B-%Y')

# Calculate two years ago and one year ago today
two_years_ago = datetime.now() - timedelta(days=365 * 2)
one_year_ago = datetime.now() - timedelta(days=365)

# Filter events for the previous year
previous_year_data = (
    df[df['EVENT_DATE2'].between(two_years_ago, one_year_ago - timedelta(days=1))]
    .groupby('COUNTRY')
    .size()
    .sort_values(ascending=False)
 
)

# Filter events for the current year
current_year_data = (
    df[df['EVENT_DATE2'] >= one_year_ago]
    .groupby('COUNTRY')
    .size()
    .sort_values(ascending=False)

)
previous_year_data = previous_year_data.reindex(current_year_data.index, fill_value=0)

# Create DataFrame for top 10 countries and events from one year ago to now
df2 = pd.DataFrame({
    'Country': current_year_data.index,
    'Events_One_Year_Ago_to_Now': current_year_data.values,
    'Percent_Change': (((current_year_data - previous_year_data) / previous_year_data) * 100).round(2)
})
print(df2)
#df2.to_csv('DataFrame.csv', index = False)
'''
'''
#Histogram
df['EVENT_DATE2'] = pd.to_datetime(df['EVENT_DATE'], format='%d-%B-%Y')
df_last_three_months = df[df['EVENT_DATE2'] >= (datetime.now() - timedelta(days=90))]
df_last_three_months.set_index('EVENT_DATE2', inplace=True)
events_per_week = df_last_three_months.resample('W-Mon').size()
average_activities_per_day = events_per_week / 7  # Assuming 7 days in a week
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(range(len(events_per_week)), events_per_week, color='skyblue', width=0.8)
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Events')
ax1.set_xticks(range(len(events_per_week)))
ax1.set_xticklabels([date.strftime('%Y-%m-%d') for date in events_per_week.index], rotation=45, ha='right')
ax2 = ax1.twinx()
ax2.plot(range(len(events_per_week)), average_activities_per_day, color='red', linestyle='--')
fig.legend(loc='upper left', bbox_to_anchor=(0.15, 0.95))
plt.title('Number of Events per Week in the Last Three Months with Average Daily Activities Line')
plt.tight_layout()
plt.show()
plt.close()

'''

