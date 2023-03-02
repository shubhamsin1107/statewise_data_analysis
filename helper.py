import pandas as pd
def state_list(df):
    state_list = df['state'].unique().tolist()
    state_list.sort()
    return state_list

def type_1():
    type = ['Gross State Domestic Product','Net State Domestic Product','Per Capita Income']
    return type
def type_2():
    type = ['Net domestic Product in Percent','Net Depreciation Rate in Percent','Per Capita Income']
    return type 
def type_3():
    type = ['density', 'Total Population','Capital Expenditure']
    return type


def get_dataframe(df, state, column_names):
    state_df = df[df['state'] == state]
    state_df = state_df[state_df.value != 0]
    # Return a new dataframe with only the "YEAR" and specified columns
    return state_df[['year'] + list(column_names)]


def get_state_data(df, state1, state2):
    data1 = df[df['state'] == state1].reset_index(drop=True)
    data1 = data1[data1.value !=0]
    data2 = df[df['state'] == state2].reset_index(drop=True)
    data2 = data2[data2.value!=0]
    combined_data = pd.concat([data1, data2], keys=[state1, state2]).reset_index()
    combined_data = combined_data.drop(['level_1'], axis=1)
    return combined_data


def get_state(df, state):
    state_df = df[df['state'] == state]
    state_df = state_df[state_df.value!= 0]
    return state_df


def get_top_states(state_name, type_1, type_2, df_2020):
    state_data = df_2020[df_2020['state'] == state_name]
    if type_1 != type_2:
        other_states = df_2020[df_2020['state'] != state_name].sort_values(by=type_1, ascending=False)
        top_states = other_states.head(9)
        top_10 = pd.concat([state_data, top_states])
        top_10 = top_10[['state', type_1, type_2]].sort_values(by=type_1, ascending=False)
    else:
        other_states = df_2020[df_2020['state'] != state_name].sort_values(by=type_1, ascending=False)
        top_states = other_states.head(9)
        top_10 = pd.concat([state_data, top_states])
        top_10 = top_10[['state', type_1]].sort_values(by=type_1, ascending=False)
    return top_10




def assign_zones(df_2021):
    north_zone = ['Chandigarh', 'Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Punjab', 'Rajasthan','Uttarakhand']
    east_zone = ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal']
    west_zone = ['Goa', 'Gujarat', 'Maharashtra']
    south_zone = ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana', 'Andaman & Nicobar Island', 'Puducherry']
    central_zone = ['Chhattisgarh', 'Madhya Pradesh', 'Uttar Pradesh']
    north_east_zone = ['Arunachal Pradesh','Assam','Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura' ]
    zones = {'North': north_zone, 'East': east_zone, 'West': west_zone, 'South': south_zone, 'Central': central_zone, 'North East': north_east_zone}
    
    df_with_zones = df_2021.copy()
    df_with_zones['ZONE'] = ''
    
    for zone, state_list in zones.items():
        for state in state_list:
            df_with_zones.loc[df_with_zones['state'] == state, 'ZONE'] = zone
    df_with_zones.fillna(0,inplace=True)
    df_with_zones = df_with_zones[df_with_zones.value!=0]
    return df_with_zones




















def industry_type():
    indu = ['VALUE ADDED AGRI','VALUE ADDED BANK','VALUE ADDED CONC','VALUE ADDED INDUSTRY','VALUE ADDED MANU', 'VALUE ADDED SERVICE']
    return indu

def year(df):
    year  = df['YEAR'].unique().tolist
    return year


def pop_year(pop_df):
    year = pop_df['year'].unique().tolist
    return year

def get_pop(pop_df, state):
    state_df = pop_df[pop_df['state'] == state]
    state_df = state_df[state_df['value'] != 0]
    return state_df

def pop_state(pop_df):
    state_list = pop_df['state'].unique().tolist()
    state_list.sort()
    return state_list

def pop_type():
    pop = ['State-Wise Total Population', 'Decadal Growth Rate of Population', 'Literacy Rate']
    return pop

