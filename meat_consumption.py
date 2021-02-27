import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

@st.cache
def read_data():
    data = pd.read_csv('meat_consumption_2.csv')
    return data

data = read_data()

def main():
    st.title('Meat Consumption World Dashboard')
    st.sidebar.header("Parameters")
    st.markdown('''### **Introduction**
This is a dashboard for meat consumption in kg per capita. The data includes 4 meats ( pig, beef, poultry,sheep), 
around forty countries, and for the years 1990-2018. \n
This interactive dashboarad has following filters: \n
1. Meat
2. Second
3. Region
4. Sub-region
5. Country
6. Year

'''   )
    global data
    x = user_input_features()
    if not x.empty:
        #st.write(x)
        #st.write(x)
        #st.write(x.head())
        st.markdown(''' ### **Bar Graph for Distribution of Meats**
        ''')
        graph2 = meat_distribution(x)
        st.plotly_chart(graph2)
        st.markdown(''' ### **Heatmap for Distribution of Meats by Countries**
          ''')
        graph3 = heatmaps(x)
        st.plotly_chart(graph3)
        st.markdown(''' ### **Group Bar Graph for Distribution of Meats by Region/Sub-region/Country**
              ''')
        oh = st.radio('Group by:', ['Region', 'Sub-region', 'Country'])
        graph1 = region(x, oh)

        st.plotly_chart(graph1)




def heatmaps(df):

    hmap = df.groupby(['Country', 'SUBJECT'])[['Consumption kg_cap']].agg(['mean'])
    hmap.reset_index(inplace=True)
    hmap.columns = ['Country', 'SUBJECT', 'Consumption kg_cap']
    heat_df = hmap.pivot(index='Country', columns='SUBJECT', values='Consumption kg_cap')
    z = np.round(heat_df.to_numpy(), 2)

    x = list(heat_df.columns)
    y = list(heat_df.index)

    fig = ff.create_annotated_heatmap(z, x=x, y=y, colorscale='Viridis')
    fig.update_layout(legend=dict(font=dict(size=12)),
                      width=900,
                      height=700,
                      title=dict(text='Meat consumption KG per capita by countries', x=0.5, font=dict(color='black')),
                      paper_bgcolor='#F6F6F6',
                      plot_bgcolor='#F6F6F6',
                      )
    return fig

def region(df,mode='Region'):
    temp = df.groupby(['region', 'sub-region','Country', 'TIME', 'SUBJECT'])[['Consumption kg_cap', 'Population']].agg(['sum'])
    temp.reset_index(inplace=True)
    temp.columns = ['Region','Sub-region','Country','TIME','SUBJECT','Consumption kg_cap','Population']


    #st.write(temp)
    fig = px.bar(temp, x='SUBJECT', y="Consumption kg_cap", animation_frame="TIME",
                 color=mode, barmode='group',hover_name='Country',
                 color_discrete_sequence=px.colors.qualitative.Prism)#.for_each_trace(lambda t: t.update(name=t.name.split('=')[1]))
    fig.update_layout(legend=dict(font=dict(size=12)),
                      width=900,
                      height=700    ,
                      #  hover ,
                      title=dict(text='Meat consumption KG per capita by regions', x=0.5, font=dict(color='black')),
                      xaxis=dict(showgrid=False,
                                 title=mode,
                                 # type='log',
                                 color='black'

                                 ),
                      yaxis=dict(showgrid=False,
                                 title='Kg Per Capita',
                                 color='black',
                                 ),

                      paper_bgcolor='#F6F6F6',
                      plot_bgcolor='#F6F6F6',
                      )
    return fig

def meat_distribution(df):
    data_agg = df.groupby(['SUBJECT'])['Consumption kg_cap'].agg(['sum', 'mean'])
    data_agg.columns = ['total Consumption kg_cap', 'avg Consumption kg_cap']
    data_agg.reset_index(inplace=True)
    fig = px.bar(data_agg, x='SUBJECT', y='avg Consumption kg_cap',
                 title='Meat consumption KG per capita',
                 labels={'total Consumption kg_cap': 'Kg Per Capita', 'x': 'Type of Meat'}
                 )

    fig.update_layout(showlegend=False,
                      #  hover ,
                      title=dict(text='Meat consumption KG per capita', x=0.5, font=dict(color='black')),
                      xaxis=dict(showgrid=False,
                                 title='Types of Meat',
                                 # type='log',
                                 color='black'

                                 ),
                      yaxis=dict(showgrid=False,
                                 title='Kg Per Capita',
                                 color='black',
                                 ),

                      paper_bgcolor='#F6F6F6',
                      plot_bgcolor='#F6F6F6',
                      )
    return(fig)


def user_input_features():
    global data

    selected_all = st.sidebar.radio('Data: ', ['All', 'Filters'])
    if selected_all == 'All':
        return data

    selected_meat = st.sidebar.multiselect('Meat',
                                           list(data['SUBJECT'].unique()),
                                           list(data['SUBJECT'].unique()))
    if not selected_meat:
        st.error('Select Meat')
        return pd.DataFrame()
    filter_meat = data['SUBJECT'].isin(selected_meat)
    features = data.loc[filter_meat]

    selected_region = st.sidebar.multiselect('Region',
                                             list(features['region'].unique()),
                                             list(features['region'].unique()))
    if not selected_region:
        st.error('Select Region')
        return pd.DataFrame()
    filter_region = features['region'].isin(selected_region)
    features = features.loc[filter_region]

    selected_sub_region = st.sidebar.multiselect('Sub-Region',
                                                 list(features['sub-region'].unique()),
                                                 list(features['sub-region'].unique()))
    if not selected_sub_region:
        st.error('Select Sub-Region')
        return pd.DataFrame()
    filter_sub_region = features['sub-region'].isin(selected_sub_region)
    features = features.loc[filter_sub_region]

    selected_country = st.sidebar.multiselect('Country', list(features['Country'].unique()),
                                              list(features['Country'].unique()))
    if not selected_country:
        st.error('Select Country')
        return pd.DataFrame()
    filter_country = features['Country'].isin(selected_country)
    features = features.loc[filter_country]

    selected_years = st.sidebar.slider('Year', min_value=min(features['TIME']), max_value=max(features['TIME']),
                              value = (min(features['TIME']),max(features['TIME'])), step=1)
    years =[i for i in range(selected_years[0],selected_years[1]+1)]

    filter_years = features['TIME'].isin(years)


    features = features.loc[filter_years]

    return features


if __name__ == "__main__":
    main()
