import pandas as pd
import streamlit as st
@st.cache_data
def preprocess(df):
    year = [col for col in df.columns if col.isnumeric()]
    df = pd.melt(df, id_vars=['state','CATEGORY'], value_vars=year, var_name='year', value_name='value')
    df['value'].fillna(0, inplace=True)
    df['value'] = df['value'].astype(int)
    df = pd.concat([df, pd.get_dummies(df['CATEGORY'])], axis = 1)
    for i in range(len(df)):
        if df.iloc[i, 3] != 0:
            for j in range(4, 23):
                if df.iloc[i, j] == 1:
                    df.iat[i, j] = df.iloc[i, 3]
                    break
        else:
            for j in range(4, 23):
                if df.iloc[i, j] == 1:
                    df.iloc[i, j] = 0
                    break
    df = df.groupby(['state','year']).sum(numeric_only=True).reset_index()
    
    return df

@st.cache_data
def preprocess1(pop_df):
    year_pop = [col for col in pop_df.columns if col.isnumeric()]
    pop_df = pd.melt(pop_df, id_vars=['state','data'], value_vars=year_pop, var_name='year', value_name='value')
    pop_df['value'].fillna(0, inplace=True)
    pop_df = pd.concat([pop_df, pd.get_dummies(pop_df['data'])], axis = 1)

    for i in range(len(pop_df)):
        if pop_df.iloc[i, 3] != 0:
            for j in range(4, 12):
                if pop_df.iloc[i, j] == 1:
                    pop_df.iat[i, j] = pop_df.iloc[i, 3]
                    break
        else:
            for j in range(4, 12):
                if pop_df.iloc[i, j] == 1:
                    pop_df.iloc[i, j] = 0
                    break
    pop_df[['Decadal Growth', 'Literacy Rate','Population in Rural Area','Population in Urban Area','Sex Ratio','Total Population','density']] = pop_df[['Decadal Growth', 'Literacy Rate','Population in Rural Area','Population in Urban Area','Sex Ratio','Total Population','density']].astype('float64')
    pop_df = pop_df.groupby(['state','year']).sum(numeric_only=True).reset_index()
    return pop_df

@st.cache_data
def preprocess2(df, pop_df):
    df_2021 = df[df['year'] == '2021']
    pop_2021 = pop_df[pop_df['year'] =='2021']
    df_2021 = pd.merge(df_2021, pop_2021[['state','Total Population','density']],on='state', how='outer')
    total_nsdp = df_2021['Net State Domestic Product'].sum()
    df_2021['Net domestic Product in Percent'] = round((df_2021['Net State Domestic Product'] / total_nsdp) * 100,2)
    return df_2021

@st.cache_data
def preprocess3(india_state,df_2021):
    name_mapping = {'Arunanchal Pradesh': 'Arunachal Pradesh','NCT of Delhi': 'Delhi', 'Dadara & Nagar Havelli':'Dadara & Nagar Haveli'}

    for feature in india_state['features']:
        state_name = feature['properties']['st_nm']
        if state_name in name_mapping:
            feature['properties']['st_nm'] = name_mapping[state_name]

    state_id_map = {}
    for feature in india_state['features']:
        feature['state_code'] = feature['properties']['state_code']
        state_id_map[feature['properties']['st_nm']] = feature['state_code']
    df_2021['state_code'] = df_2021['state'].apply(lambda x: state_id_map[x])
    return df_2021

@st.cache_data
def for_ranking(df):
    df_2020 = df[df['year'] == '2020']
    df_2020['nsdp/gsdp'] = df_2020['Net State Domestic Product'] / df_2020['Gross State Domestic Product']
    df_2020['Net Depreciation Rate in Percent'] = round((100 -df_2020['nsdp/gsdp']*100),2)
    total_nsdp = df_2020['Net State Domestic Product'].sum()
    df_2020['Net domestic Product in Percent'] = round((df_2020['Net State Domestic Product'] / total_nsdp) * 100,2)
    return df_2020