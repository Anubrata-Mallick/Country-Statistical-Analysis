'''
Title: Helper Function Store
Description: Collection of functions which is made for doing small sub tasks to construct a route
'''

import plotly.express as px
import plotly.graph_objects as go


#Helper Functions
def bubbleMaker(x):
    if x < 0:
        return 5
    else:
        return x*20
    
def Overall_region(df, region, col):
    
    if region == 'Overall' and col=='No column':
        temp_df = df
        
    elif region != 'Overall' and col == 'No column':
        temp_df = df[df['Region']==region]
        
    elif region == 'Overall' and col != 'No column':
        temp_df = df.sort_values(col, ascending=False)
        
    elif region != 'Overall' and col != 'No column':
        temp_df = df[df['Region']==region].sort_values(col, ascending=False)
    
    temp_df = temp_df.reset_index().drop(columns=['index', 'Region'])
    return temp_df


#Function store
def region_wise_piechart(Overalldf, region, col):
    #filter
    others_df = Overall_region(Overalldf, region, col)

    # if df become huge then compress it
    if others_df.size > 4:
        others_gdp = others_df['GDP'].sum().astype('int') - others_df["GDP"].head(5).sum().astype(int)
        others_population = others_df['Population(Thousand)'].sum().astype('int') - others_df["Population(Thousand)"].head(5).sum().astype(int)
        others_TS = others_df['Threatened species'].astype('float').sum() - others_df["Threatened species"].astype('float').head(5).sum()
        others_TM = others_df['Total Migrants'].astype('float').sum() - others_df["Total Migrants"].head(5).astype('float').sum()
        others_df = others_df.head(4)

        new_row = ['others', others_population, others_gdp, '0.0', others_TS, others_TM]
        others_df.loc[-1] = new_row
        others_df.reset_index(drop=True, inplace = True)
    
    fig = px.pie(others_df, names='country', values=col)
    
    return fig


def GDP_Bubble(GDP_df, region):
    temp_df = GDP_df[GDP_df['Region']==region]
    temp_df['GDP growth'] = temp_df['GDP growth'].astype('float').apply(bubbleMaker)
    y = temp_df['GDP']
    x = temp_df['GDP/capita']
    marker_size = temp_df['GDP growth']
    text_labels = temp_df['country']
    # Create the bubble chart using go.Scatter
    fig = go.Figure(data=go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=marker_size,
            showscale=False,
        ),
        text=text_labels
    ))

    # Customize the chart (optional)
    fig.update_layout(
        title="GDP vs GDP per Capita vs GDP Growth",
        xaxis_title="GDP/Capita",
        yaxis_title="GDP",
        height = 600,
    )

    return fig


def Regional_GDP_Distribution(Economy_df, region):
    temp_df = Economy_df[Economy_df['Region']==region]
    temp_df['Agriculture'] = temp_df['Agriculture'].astype('float')


    x_df = temp_df.sum()[['Agriculture','Industry', 'Services']].reset_index()
    x_df ['count'] = x_df.shape[0]
    x_df[0] = x_df[0].apply(lambda x: (x/temp_df.shape[0]))


    fig = px.pie(x_df, names='index', values=0, title=f'{region} GDP')
    return fig


def GDP_Distribution(Economy_df, region):
    temp_df = Economy_df[Economy_df['Region']==region]
    temp_df['Agriculture'] = temp_df['Agriculture'].astype('float')
    categories = temp_df['country']
    values1 = temp_df['Agriculture']
    values2 = temp_df['Industry']
    values3 = temp_df['Services']

    # Create a Figure with two traces (two sets of bars)
    fig = go.Figure(data=[
        go.Bar(name='Agriculture', x=categories, y=values1),
        go.Bar(name='Industry', x=categories, y=values2),
        go.Bar(name='Services', x=categories, y=values3)
    ])

    # Set the barmode to 'stack' for a stacked bar plot
    fig.update_layout(barmode='stack')

    # Customize the chart (optional)
    fig.update_layout(
        title="GDP distribution in Economy",
        xaxis_title="Sectors",
        yaxis_title="Countries"
    )
    return fig


def Economy_vs_Employment(Economy_df, Employment_df, region):
    compare = Economy_df.merge(Employment_df, on=['country','Region'], how='left')
    compare = compare[compare['Region']==region]
    # Agriculture
    categories = compare['country']
    group1 = compare['Agriculture']
    group2 = compare['emp_Agriculture']

    Agriculture = go.Figure(data=[
        go.Bar(name='Economy', x=categories, y=group1, text=group1, textposition='inside', offsetgroup=0),
        go.Bar(name='Employment', x=categories, y=group2, text=group2, textposition='inside', offsetgroup=1)
    ])

    Agriculture.update_layout(
        title="Agriculture",
        xaxis_title="Countries",
        yaxis_title="Scale",
        barmode='group' 
    )
    #Industry
    categories = compare['country']
    group1 = compare['Industry']
    group2 = compare['emp_Industry']

    Industry = go.Figure(data=[
        go.Bar(name='Economy', x=categories, y=group1, text=group1, textposition='inside', offsetgroup=0),
        go.Bar(name='Employment', x=categories, y=group2, text=group2, textposition='inside', offsetgroup=1)
    ])

    Industry.update_layout(
        title="Industry",
        xaxis_title="Countries",
        yaxis_title="Scale",
        barmode='group'  
    )
    #Services
    categories = compare['country']
    group1 = compare['Services']
    group2 = compare['emp_Services']

    Services = go.Figure(data=[
        go.Bar(name='Economy', x=categories, y=group1, text=group1, textposition='inside', offsetgroup=0),
        go.Bar(name='Employment', x=categories, y=group2, text=group2, textposition='inside', offsetgroup=1)
    ])

    Services.update_layout(
        title="Services",
        xaxis_title="Countries",
        yaxis_title="Scale",
        barmode='group'  
    )

    return Agriculture, Industry, Services


def Trade(Trade_df, region, col):
    x = Trade_df[Trade_df['Region'] == region]
    x = x.sort_values(col, ascending=False)
    x.drop(columns=['Region'], inplace = True)
    return x.reset_index(drop=True)


def Region_pi(edtech):
    edtech['Mobile'] = edtech['Mobile'].astype('float')
    edtech['Internet'] = edtech['Internet'].astype('int')
    edtech['Primary_f'] = edtech['Primary_f'].astype('float')
    edtech['Primary_m'] = edtech['Primary_m'].astype('int')
    edtech['Secondary_f'] = edtech['Secondary_f'].astype('float')
    edtech['Secondary_m'] = edtech['Secondary_m'].astype('int')
    edtech['Tertiary_f'] = edtech['Tertiary_f'].astype('float')
    edtech['Tertiary_m'] = edtech['Tertiary_m'].astype('int')

    piechart = edtech.drop(columns='country')
    piechart.groupby('Region').mean()

    mobile = px.pie(piechart, names='Region', values='Mobile', title="Mobile Subscription")
    internet = px.pie(piechart, names='Region', values='Internet', title="Internet Subscription")

    return mobile, internet


def createbar(df, col, title):
    categories = df['country']
    group1 = df[col]

    fig = go.Figure(data=[
        go.Bar(name='Economy', x=categories, y=group1, text=group1, textposition='inside', offsetgroup=0),
    ])

    fig.update_layout(
        title=title,
        xaxis_title="Countries",
        yaxis_title="Scale",
    )
    return fig


def compare(edtech_r, m, f, title):
    categories = edtech_r['country']
    group1 = edtech_r[m]
    group2 = edtech_r[f]

    # Create a grouped bar chart
    fig = go.Figure(data=[
        go.Bar(name='Male', x=categories, y=group1, text=group1, textposition='inside', offsetgroup=0),
        go.Bar(name='Female', x=categories, y=group2, text=group2, textposition='inside', offsetgroup=1)
    ])

    # Customize the chart (optional)
    fig.update_layout(
        title= title,
        xaxis_title="Countries",
        yaxis_title="Scale",
        barmode='group'  # Set the barmode to 'group' for grouped bars
    )

    return fig

    
def barplot(gender, df):
    if gender == 'Male':
        p = createbar(df, 'Primary_m', 'Pimary Education')
        s = createbar(df, 'Secondary_m', 'Secondary Education')
        t = createbar(df, 'Tertiary_m', 'Tertiary Education')
    elif gender == 'Female':
        p = createbar(df, 'Primary_f', 'Pimary Education')
        s = createbar(df, 'Secondary_f', 'Secondary Education')
        t = createbar(df, 'Tertiary_f', 'Tertiary Education')
    else:
        p = compare(df,'Primary_m', 'Primary_f', 'Pimary Education')
        s = compare(df,'Secondary_m' ,'Secondary_f', 'Secondary Education')
        t = compare(df,'Tertiary_m', 'Tertiary_f', 'Tertiary Education')
    return p,s,t

