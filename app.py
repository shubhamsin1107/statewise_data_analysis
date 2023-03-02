import numpy as np
import streamlit as st
import pandas as pd
import preprocessor,helper
from plotly import express as px, figure_factory as ff, subplots as sp, graph_objects as go
import matplotlib.pyplot as plt
import json


# setting page layout
st.set_page_config(layout="wide")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('NET VS GROSS GDP', 'INDUSTRY WISE COMPARISON', 'POPULATION COMPARISON')
)
# importing data
df = pd.read_csv('DATA.csv')
pop_df = pd.read_csv('population.csv')
india_state = json.load(open('states_india.geojson','r'))
df = preprocessor.preprocess(df)
pop_df = preprocessor.preprocess1(pop_df)
df_2021 = preprocessor.preprocess2(df,pop_df)
df_2020 = preprocessor.for_ranking(df)

# importing data from helper
state = helper.state_list(df)
type = helper.type_1()
type2 = helper.type_2()
type3 = helper.type_3()

#getting user input
selected_state = st.sidebar.selectbox('SELECT STATE', state)



if user_menu == 'NET VS GROSS GDP':
    st.header('About Data used')
    st.markdown('○ :orange[Gross State Domestic Product (GSDP)] at Constant price is a measure of the economic output of a state which includes all the industries.')
    st.write('○ :orange[Net State Domestic product (NSDP)] at Constant price is similar to GSDP however it takes into account depreciation of fixed capital assets.')
    st.markdown('○ In simple terms :green[NSDP =  GSDP - Depreciation].')
    st.write('---')

    # Get user input
    selected_type_1 = st.sidebar.selectbox('SELECT TYPE', type)
    other_state = st.selectbox('Select Another State', ['None'] + state, index=3)

    # Get state data
    state_vs_state = helper.get_state_data(df,selected_state, other_state)
    state_df = helper.get_state(df, selected_state)
    state_df1 = helper.get_state(df, other_state) if other_state != 'None' else None
    
    # Generate line chart
    st.caption('GSDP and NSDP are in Crores and Per Capita Income is in ₹')
    fig = px.line(state_vs_state, x='year', y=selected_type_1, color='state', markers=True)
    if state_df1 is not None:
        fig.update_layout(title=f'Comparison between {selected_state} and {other_state}', title_font =dict(size=24),
                        width=1000, height=400, xaxis_title='Year',
                        yaxis_title=f'{selected_type_1}')
    else:
        fig.update_layout(title=f'{selected_type_1} of {selected_state}',
                        width=1000, height=400, xaxis_title='Year',title_font =dict(size=24),
                        yaxis_title=f'{selected_type_1}')
    st.plotly_chart(fig)

    # Calculate CAGR
    n_years = len(state_df) - 1
    gsdp_cagr = (state_df[selected_type_1].iloc[-1] / state_df[selected_type_1].iloc[0]) ** (1/n_years) - 1
    nsdp_cagr = (state_df1[selected_type_1].iloc[-1] / state_df1[selected_type_1].iloc[0]) ** (1/n_years) - 1 if state_df1 is not None else None
    
    # Display CAGR
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label = f"{selected_state}'s CAGR :", value =  f"{round(gsdp_cagr * 100, 2)}%",delta=None)
    with col2:
        if nsdp_cagr is not None:
            st.metric(label = f"{other_state}'s CAGR :",value = f"{round(nsdp_cagr * 100, 2)}%" ,delta=None)

    #Get data for selected type
    type_df = df_2020[['state', selected_type_1]]
    type_df = type_df.set_index('state')

    # Sort data by selected type column
    sorted_df = type_df.sort_values(selected_type_1, ascending=False)

    # Get rank of other state
    other_state_rank = sorted_df.index.get_loc(selected_state) + 1

    # Display rank
    st.header('Some insights that can be derived from the chart are:')
    st.markdown(f"1. :blue[{selected_state}] ranks {other_state_rank} in {selected_type_1} as on 2020")
    st.write('2. As on 2021 :blue[Maharashtra, Gujarat and Tamil Nadu] were the top in both Gross and Net production respectively contributing nearly 30% total output.')
    st.write('3. As on 2020 :green[Goa, Delhi and Sikkim] had highest Per Capita Income and :red[Manipur, Uttar Pradesh and Bihar] were at the bottom of the list ranking at 31, 32 and 33 respectively.')
    st.write('---')

    st.header('About Data used')
    st.markdown("○ :orange[Net Domestic Product in percent] is state's individual  contribution in  India's GDP in percent.")
    st.write('○ :orange[Net Depreciation rate] is the ratio between GSDP/NSDP which indicates the extent of capital goods replaced in economy.')
    st.write('---')

    #bar chart
    selected_type_2 = st.selectbox('SELECT TYPE', type2)
    top = helper.get_top_states(selected_state,selected_type_1,selected_type_2,df_2020)
    x = top['state']
    y1 = top[selected_type_1]
    y2 = top[selected_type_2]

    if selected_type_1 == selected_type_2:
            fig = go.Figure(data=[go.Bar(name=selected_type_1, x=x, y=y1, width=0.2, offset=-0.1, marker=dict(color=['#636EFA' if state != selected_state else '#60d394' for state in x]))])
            fig.update_layout(title=f'{selected_type_1} for Top 10 States',width=1000, height=500,
                            yaxis=dict(title=f'{selected_type_1}', rangemode='tozero'), yaxis_showgrid=False,)
            st.plotly_chart(fig)           
    else:
        fig = go.Figure(data=[go.Bar(name=selected_type_1, x=x, y=y1, width=0.2, offset=-0.1, hovertext=y1, marker=dict(color=['#636EFA' if state != selected_state else '#60d394' for state in x]))])
        fig.add_trace(go.Bar(name=selected_type_2, x=x, y=y2, yaxis='y2', width=0.2,offset=0.1, hovertext=y2, marker=dict(color=['#ef798a' if state != selected_state else '#f46036' for state in x])))
        fig.update_layout(title=f'{selected_type_1} and {selected_type_2} for Top 10 States',width=1000, height=500,
                            yaxis=dict(title=f'{selected_type_1}', rangemode='tozero'), yaxis_showgrid=False,
                            yaxis2=dict(title=f'{selected_type_2}', overlaying='y'   , side='right', rangemode='tozero'),legend=dict(y=1.1, orientation='h'))
        st.plotly_chart(fig)
    st.write('Some insights that can be derived from the chart are:')
    st.write('1. Among all the states, Goa has the highest Per Capita Income. This means that Goa has a larger share of the total NSDP of all states, despite having a smaller population.')
    st.write('2. Delhi has the 2nd highest Per Capita Income among the top 5 states, followed by Sikkim Chandigarh and Haryana. This indicates that these states have a higher economic output per person relative to the other states.')
    st.write('3. Mizoram and Arunachal Pradesh have the lowest per capita NSDP among the top 5 states, despite having a higher NSDP percentage than some other states. This could be due to their smaller population and/or lower overall NSDP.')
    st.write('4. There is a significant difference in per capita NSDP between the top 5 states and the rest of the states. The top 5 states have a per capita NSDP ranging from Rs. 3.2 lakhs to Rs. 5.6 lakhs, while the rest of the states have a per capita NSDP of less than Rs. 2.2 lakhs. This indicates that the top 5 states have a more developed economy compared to the rest of the states.')
    st.write('5. Net Depreciation Rate of major states is around 10%. The rate Jammu & Kashmir and Sikkim is 20% and 14% respectively. ')
    st.write('---')


     
    #scatter plot
    selected_type_3 = st.selectbox('SELECT TYPE',type3 )
    zones_df = helper.assign_zones(df_2021)
    fig.update_layout(width=1000, height=500)

    if selected_type_3 == 'density':
        if selected_type_1 == 'Per Capita Income':
            fig = px.scatter(zones_df, x=selected_type_1, y =selected_type_3 ,size =selected_type_3, color='ZONE',size_max=70, hover_name='state')
            fig.update_xaxes(tickformat=',.0f', tickprefix='₹')
            st.plotly_chart(fig,use_container_width=True)
            st.write('1. Delhi and Chandigarh have 11.3k and 9.2k density respectively with high Per capita income.')
            st.write('2. Most of the big states in India have under 1000 People/Km and small states are mostly under 500 People/km. ')
            st.write('3. Per capita income for most states ranges from 27k Rs to 160k Rs. where Easter and North eastern states are in lower range and Souther states being in middle range.  ')
        else:
            fig = px.scatter(zones_df, x=selected_type_1, y =selected_type_3 ,size =selected_type_1, color='ZONE',size_max=70, hover_name='state')
            fig.update_xaxes(tickformat=',.0f', tickprefix='₹', ticksuffix=' Cr')
            st.plotly_chart(fig,use_container_width=True)
            st.write('1. Most state with high Gdp output has under 600 Density, Uttar Pradesh being expecption has 829  density and maharastra being at the top of Gdp output.')
            st.write('2. Middle Gdp output states ranges from 200 to 1000 density and 4 lakh crore to 8 lakh crore in Gdp output.')
            st.write('3. Lower Gdp output states mostly have Norther Eastern states and North states mostly because of higher altitude areas and tough terrains')
    elif selected_type_3 == 'Total Population':
        if selected_type_1 == 'Per Capita Income':
            fig = px.scatter(zones_df, x=selected_type_3, y =selected_type_1 ,size =selected_type_3, color='ZONE',size_max=70, hover_name='state')
            fig.update_xaxes( tickmode='array',tickvals= [0,50000,100000,150000,200000,250000],ticktext=['0','5cr', '10cr', '15cr', '20cr', '25Cr'])
            st.plotly_chart(fig,use_container_width=True)
            st.write('1. All North east states except Assam has population under 60 Lakh and Per capita income under 1 lakh except Sikkim which is 2.4 lakh.')
            st.write("2. Northern State's population ranges from 1 Cr. to 7 Cr. depending on the economic development of state. Delhi being highest in per capita income with 2.4 Lakh and Jammu & Kashmir at lowest with Rs 65k" )
            st.write("3. Eastern states having middle to high population ranging from 4 Cr. to 12 Cr. With average per capita income lowest comparing with other zones.")
            st.write("4. Per capita income of souther states ranges from 1.1 Lakh to 1.6 Lakh and Population between 8 Cr. to 3.5 Cr.")
            st.write("5. Uttar pradesh being at lower capita with high population and Goa at higher per capita with low population in thier respective zones.")
        else:
            fig = px.scatter(zones_df, x=selected_type_3, y =selected_type_1 ,size =selected_type_1, color='ZONE',size_max=60, hover_name='state')
            fig.update_yaxes(tickformat=',.0f', tickprefix='₹', ticksuffix=' Cr')
            fig.update_xaxes( tickmode='array',tickvals= [0,50000,100000,150000,200000,250000],ticktext=['0','5cr', '10cr', '15cr', '20cr', '25Cr'])
            st.plotly_chart(fig,use_container_width=True) 
            st.write('1. Most states with population over 5Cr. has economic output of 50 billion Dollar and more with Maharastra at top. Bihar being exception with 12 Cr. and economic output lower then 50 Billion Dollar') 
            st.write("2. Assam at top with highest economic output in northern zone with 20 billion dollars approximately.")
            st.write("3. Northern states having lower to middle economic output ranging from 1 billion dollar to 60 billion dollar.")
    else:
        if selected_type_1 == 'Per Capita Income':
            fig = px.scatter(zones_df, x=selected_type_1, y =selected_type_3 ,size =selected_type_3, color='ZONE',size_max=60, hover_name='state')
            fig.update_yaxes( tickmode='array',tickvals= [0,50000,100000,150000,200000,250000],ticktext=['0','50000cr', '1 Lakh cr', '1.5 Lakh cr', '2 Lakh cr', '2.5 Lakh cr'])
            fig.update_xaxes(tickformat=',.0f')
            st.plotly_chart(fig,use_container_width=True)
            # st.write    


    st.write('---')










    #choropleth map
    india_df = preprocessor.preprocess3(india_state, df_2021)
    fig = px.choropleth_mapbox(india_df, geojson=india_state, locations='state_code',
                            featureidkey='properties.state_code',
                            color=selected_type_1,color_continuous_scale=px.colors.sequential.Plasma,
                            mapbox_style="carto-positron",
                            center={"lat": 21.7679, "lon": 78.9629},
                            zoom=3, hover_name='state',
                            opacity=0.5
                            )
    fig.update_layout(width=1000, height=700)
    st.plotly_chart(fig)

if user_menu == 'INDUSTRY WISE COMPARISON':
    pass












if user_menu == 'INDUSTRY WISE COMPARISON':
    state = helper.state_list(df)
    type = helper.industry_type()
    year = helper.year(df)
    selected_state = st.sidebar.selectbox('SELECT STATE', state)
    selected_columns = st.multiselect("Select to check",type)
    industry = helper.get_state(df,selected_state)

    # LINE CHART
    if selected_columns:                                     
        chart_data = industry[['YEAR'] + selected_columns]
        fig = px.line(chart_data, x='YEAR', y=selected_columns)
        st.plotly_chart(fig)

    # PIE chart
    if selected_columns:
        chart_data = industry[industry['YEAR'] == max(industry['YEAR'])]
        chart_data = chart_data[selected_columns].sum().reset_index()
        chart_data.columns = ['Columns', 'Value']
        fig = px.pie(chart_data, values='Value', names='Columns', title='Pie Chart for the Latest Year')
        st.plotly_chart(fig)

    #BAR CHART
    chart_data = industry[['YEAR'] + selected_columns]
    growth_rates = chart_data[selected_columns].pct_change().mean() * 100
    growth_rates = growth_rates.reset_index()
    growth_rates.columns = ['Columns', 'Growth Rate']
    growth_rates['Growth Rate'] = growth_rates['Growth Rate'].astype(int)
    fig = px.bar(growth_rates, x='Columns', y='Growth Rate', title='Average Growth Rate Over the Years',color='Growth Rate', color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig)










if user_menu == 'POPULATION COMPARISON':
    state = helper.pop_state(pop_df)
    year = helper.pop_year(pop_df)
    type = helper.pop_type()
    selected_state = st.sidebar.selectbox('Select State', state)
    selected_columns = st.selectbox("Select to check",type)
    population = helper.get_pop(pop_df,selected_state)
    
    # if selected_state:
    #     fig = px.line(population, x='year', y=selected_columns, color_discrete_sequence=['brown'])
    #     st.plotly_chart(fig)

    fig = px.line(population, x='year', y=selected_columns, 
              title='Population trend over years', 
              labels={'year': 'Year', 'selected_columns': 'Population'}, 
              color_discrete_sequence=['red'])

    fig.update_layout(annotations=[dict(x=year, y=value, text=f'increased by', 
    showarrow=True , arrowhead=1, ax=-50, ay=-50) 
    for year, value in zip(population.year, population[selected_columns])])
    st.plotly_chart(fig)


    # fig = px.scatter_mapbox(population, lat='latitude', lon='longitude', 
    #                     color=selected_columns, size=selected_columns,
    #                     color_continuous_scale='Viridis', size_max=15, 
    #                     title='Population trend over years')
    



