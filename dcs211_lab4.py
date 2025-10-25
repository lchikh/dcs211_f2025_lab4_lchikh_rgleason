
import pandas as pd
from prettytable import PrettyTable as pt
filename="county_economic_status_2024.csv"
# skipping dscriptive rows at top and unecessary bottom rows
df = pd.read_csv(filename, skiprows = 5, 
skipfooter = 2, engine = "python", thousands = ',')
#resetting the index so hat it runs from 0
df = df.reset_index(drop=True)
#renaming the coumns to meaningful names
df.columns=["fips","state","county","arc_county","econ_status24","three_yr_avg_unemp_rate19_21","income21","poverty17_21","three_yr_avg_unemp_rate_US19_21","PCMI_US21","PCMI_US_inv21","poverty_US17_21","comp_index_val24","index_val_rank24","quartile24"]

print(type(df["state"]))
# type of df['states' is <class 'pandas.core.series.Series'>

#printing the number of counties of each state using value_counts
print(df["state"].value_counts())
top_ten_states=df["state"].value_counts()[0:10]

print(top_ten_states)

# Create a new table
table_one = pt()
table_one.field_names = ["State", "# counties" , "PCI (mean)" , "PCI (median)" , "Poverty Rate"]


#for state in top_ten_states:
#   print(top_ten_states[0])
by_state = df.groupby("state")

#printing top ten states with mean and median income per capita as well as avg poverty rate
for i in range(len(top_ten_states)):
    state = top_ten_states.index[i]
    number_of_counties = len(by_state.get_group(state))
    income_mean = by_state.get_group(state)['income21'].mean()
    income_median = by_state.get_group(state)['income21'].median()
    poverty = by_state.get_group(state)['poverty17_21'].mean()

    table_one.add_row([state, number_of_counties,f"{income_mean:.2f}",f"{income_median:.2f}",f"{poverty:.2f}"])

print(table_one)

#grouping the bottom 10 states
bottom_ten_states=df["state"].value_counts()[-11:-1]
print(bottom_ten_states)
#setting up table_two for the bottom 10 states
table_two = pt()
table_two.field_names = ["State", "# counties" , "PCI (mean)" , "PCI (median)" , "Poverty Rate"]

#printing top ten states with mean and median income per capita as well as avg poverty rate
for i in range(len(bottom_ten_states)):
    state = bottom_ten_states.index[i]
    number_of_counties = len(by_state.get_group(state))
    income_mean = by_state.get_group(state)['income21'].mean()
    income_median = by_state.get_group(state)['income21'].median()
    poverty = by_state.get_group(state)['poverty17_21'].mean()

    table_two.add_row([state, number_of_counties,f"{income_mean:.2f}",f"{income_median:.2f}",f"{poverty:.2f}"])


print(table_two)

#setting third table for top ten counties by decreasing poverty rate

table_three = pt()
table_three.field_names = ["State", "Counties" , "PCI" , "Poverty Rate" , "Avg Unemployment"]

state="South Dakota"
#this will show all info for specific state
print(df.groupby("state").get_group("South Dakota"))
#now prints the poverty for that specific state
counties_by_poverty= df.groupby("state").get_group("South Dakota")["poverty17_21"]
counties_by_poverty = counties_by_poverty.reset_index(drop=True)
#turn it into a list
counties_by_poverty_list=counties_by_poverty.tolist()
for i in range (10):
    index= counties_by_poverty_list.index(max(counties_by_poverty_list))
    counties=df.groupby("state").get_group("South Dakota")["county"]
    pci=df.groupby("state").get_group("South Dakota")["income21"]
    pov_rate=df.groupby("state").get_group("South Dakota")["poverty17_21"]
    avg_unemployment=df.groupby("state").get_group("South Dakota")["three_yr_avg_unemp_rate19_21"]
    table_three.add_row(["North Carolina", counties.iloc[index], f"{pci.iloc[index]:.2f}", f"{pov_rate.iloc[index]:.2f}",f"{avg_unemployment.iloc[index]:.2f}"])
    counties_by_poverty_list=counties_by_poverty_list[:index] + counties_by_poverty_list[index+1:]
print(table_three)

















