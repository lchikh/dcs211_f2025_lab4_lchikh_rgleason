
import pandas as pd
import matplotlib.pyplot as plt 
from prettytable import PrettyTable as pt

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


filename="county_economic_status_2024.csv"
# skipping dscriptive rows at top and unecessary bottom rows
df = pd.read_csv(filename, skiprows = 5, 
skipfooter = 2, engine = "python", thousands = ',')
#resetting the index so hat it runs from 0
df = df.reset_index(drop=True)
#renaming the coumns to meaningful names
df.columns=["fips","state","county","arc_county","econ_status24","three_yr_avg_unemp_rate19_21","income21","poverty17_21","three_yr_avg_unemp_rate_US19_21","PCMI_US21","PCMI_US_inv21","poverty_US17_21","comp_index_val24","index_val_rank24","quartile24"]

#printing the mean median maximum and minimum of poverty rate across all file

print(f"the mean of the the poverty rate is : {round(df['poverty17_21'].mean(), 2)}")
print(f"the median of the the poverty rate is : {df['poverty17_21'].median()}")
print(f"the maximum of the the poverty rate is : {df['poverty17_21'].max()}")
print(f"the minimum of the the poverty rate is : {df['poverty17_21'].min()}")


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

def printTableBy(df: pd.DataFrame, field: str, how_many: int, title: str)-> None:
    """
    Prints a PrettyTable of the top and bottom 'how_many' counties
    based on a chosen field (e.g., 'poverty17_21', 'income21', or 'three_yr_avg_unemp_rate19_21').

    Parameters:
    df (pd.DataFrame): The DataFrame containing county-level economic data.
             
    field (str): Column name to sort by (e.g., 'poverty17_21', 'income21',or 'three_yr_avg_unemp_rate19_21').
    
    how_many (int): Number of top and bottom rows to include in the output. 
    
    
    title (str): Title printed above the PrettyTable.   

    Returns: None
    """

    # Sort by selected column 
    df_sorted = df.sort_values(by=field, ascending=False)

    # Get top and bottom rows
    top = df_sorted.head(how_many)
    bottom = df_sorted.tail(how_many).sort_values(by=field, ascending=True)

    # Create the PrettyTable
    table = pt()
    table.field_names = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]

    # Print the title
    print(title)

    # Add top rows
    for _, row in top.iterrows():
        table.add_row([
            f"{row['state']:<20}",
            f"{row['county']:<20}",
            f"{row['income21']:.2f}",
            f"{row['poverty17_21']:.2f}",
            f"{row['three_yr_avg_unemp_rate19_21']:.2f}"
        ])

    # Add a divider row
    table.add_row([""] * len(table.field_names), divider=True)

    # Add bottom rows
    for _, row in bottom.iterrows():
        table.add_row([
            f"{row['state']:<20}",
            f"{row['county']:<20}",
            f"{row['income21']:.2f}",
            f"{row['poverty17_21']:.2f}",
            f"{row['three_yr_avg_unemp_rate19_21']:.2f}"
        ])

    # Print the table
    print(table)

#Call printTableBy function

printTableBy(df, field="poverty17_21", how_many=10, title="COUNTIES BY POVERTY RATE")
printTableBy(df, field="income21", how_many=10, title="COUNTIES BY PER CAPITA INCOME")
printTableBy(df, field="three_yr_avg_unemp_rate19_21", how_many=10, title="COUNTIES BY AVERAGE UNEMPLOYMENT RATE")



def createByStateBarPlot( df: pd.DataFrame, field: str, filename: str,title: str, ylabel: str)-> None:
    """
    Create and save a per-state bar plot of the mean values of a given specified field.

    The function groups the provided DataFrame by 'state'. Then it computes the mean
    of the specified numeric field and sorts the resulting means in ascending order.
    Finally it produces a labeled bar plot using matplotlib. 

    Parameters:
        df (pd.DataFrame): The DataFrame containing county-level economic data.
        
        field (str): The column name (e.g., 'poverty17_21', 'income21', or'three_yr_avg_unemp_rate19_21') to compute and plot state means for.
        
        filename (str): The file path (e.g., 'pov_rate.png') to save the generated plot to.
        
        title (str): Title to display at the top of the figure.
       
        ylabel (str): Label for the y-axis, describing the plotted field.
   
    Returns: None
    """

    # Validate the column name
    if field not in df.columns:
        raise ValueError(f"Column '{field}' not found in DataFrame.")

    # Group by state and calculate mean of the selected field
    by_state = df.groupby("state")[field].mean().sort_values(ascending=True)

    # Replace full state names with abbreviations
    by_state.index = [us_state_abbrev[name] for name in by_state.index]

    # Create the figure and set the size
    plt.figure(figsize=(12, 6))

    # Create the bar plot
    plt.bar(by_state.index, by_state.values)

    # Add title and labels
    plt.title(title, fontsize=14, weight="bold")
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel("State", fontsize=12)

    # Rotate x-axis labels for readability
    plt.xticks(rotation=90, fontsize=9)

    # Add gridlines for better readability
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Adjust layout to avoid label cutoff
    plt.tight_layout()

    # Save the figure to file
    plt.savefig(filename, dpi=300)

    # Display the figure (optional for lab)
    plt.show()

#Call createByStateBarPlot Function 

createByStateBarPlot(df, 'poverty17_21', "pov_rate.png", "States By Poverty Rate", "Poverty Rate")
createByStateBarPlot(df, 'three_yr_avg_unemp_rate19_21', "unemp_rate.png", "States By Average Unemployment Rate", "Average Unemployment")
createByStateBarPlot(df, 'income21', "pci.png", "States By Per Capita Income", "Per Capita Income")



