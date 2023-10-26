'''
Title: Router
Description: Holds different routes of the main applications
'''

import streamlit as st

import helper
import Preprocessor as prep


def Overall_Analysis_page(df):
    Overalldf = prep.Overalldf_preprocess(df)

    region = Overalldf['Region'].unique().tolist()
    region.sort()
    col = Overalldf.columns.tolist()
    col.remove('country')
    col.remove('Region')

    # Pie chart genaretor - Part 
    st.title("Pie chart")
    col1, col2 = st.columns(2) # to make the 2 options side by side
    with col1:
        selected_region = st.selectbox('Select Region',region)
    with col2:
        selected_col = st.selectbox('Select parameter',col)

    fig = helper.region_wise_piechart(Overalldf, selected_region, selected_col)
    st.plotly_chart(fig)

    # Over all chart - Part 2
    st.title('Tabular Representation')
    region.insert(0,'Overall')
    col1, col2 = st.columns(2) # to make the 2 options side by side
    with col1:
        selected_region = st.selectbox('Filter Data w.r.t Region',region)
    with col2:
        selected_col = st.selectbox('Sort the column',col)

    table = helper.Overall_region(Overalldf, selected_region, selected_col)
    st.table(table)


def Regional_Economy_Page(df):
    GDP_df, Economy_df, Employment_df, Trade_df, extra_df = prep.RegionalEconomy_preprocess(df)
    region = GDP_df['Region'].unique().tolist()
    region.sort()
    selected_region = st.selectbox('Select Region',region)

# 🔴 Creating 1st segment
    #1. HIghest GDP of a region
    temp_df = GDP_df[GDP_df['Region']== selected_region]
    x = temp_df[temp_df['GDP']== temp_df['GDP'].max()]
    gdp_country = x.iloc[0]['country']
    GDP = x.iloc[0]['GDP']

    # 2. Highest GDP growth
    temp_df = GDP_df[GDP_df['Region']==selected_region]
    x = temp_df[temp_df['GDP growth']== temp_df['GDP growth'].max()]
    growth_country = x.iloc[0]['country']
    GDPgrowth = x.iloc[0]['GDP growth']

    # 3. Country which spend highest GDP percentage in healthcare sector
    temp_df = extra_df[extra_df['Region']==selected_region]
    x = temp_df[temp_df['Health']== temp_df['Health'].max()]
    health_country = x.iloc[0]['country']
    gdp_on_health = x.iloc[0]['Health']

    # 4. Country which spend highest GDP percentage in Education sector
    temp_df = extra_df[extra_df['Region']==selected_region]
    x = temp_df[temp_df['Education']== temp_df['Education'].max()]
    education_country = x.iloc[0]['country']
    gdp_on_education = x.iloc[0]['Education']

    col1, col2 = st.columns(2) 
    with col1:
        st.write("### Highest GDP")
        st.text(f"Country: {gdp_country}\nGDP: {GDP}")
    with col2:
        st.write("### Highest GDP Growth")
        st.text(f"Country: {growth_country}\nGDP growth: {GDPgrowth}%")

    col1, col2 = st.columns(2) 
    with col1:
        st.write("### Highest GDP allocate for Health")
        st.text(f"Country: {health_country}\nGDP: {gdp_on_health}%")
    with col2:
        st.write("### Highest GDP allocate for Education")
        st.text(f"Country: {education_country}\nGDP: {gdp_on_education}%")

# 🔴 Creating 2nd Segment
    st.title('GDP Bubble chart')
    fig = helper.GDP_Bubble(GDP_df, selected_region)
    st.plotly_chart(fig)

# 🔴 Creating 3rd segment
    st.title(f'GDP distribution of {selected_region}')
    fig = helper.Regional_GDP_Distribution(Economy_df, selected_region)
    st.plotly_chart(fig)

    st.write(f"## GDP distribution of {selected_region}'s every country")
    fig = helper.GDP_Distribution(Economy_df, selected_region)
    st.plotly_chart(fig)

# 🔴 creating 4th segment
    st.title('Economy vs Employment')
    Agg, Ind, Ser = helper.Economy_vs_Employment(Economy_df, Employment_df, selected_region)

    st.write("### Economy vs Employment of Agriculture")
    st.plotly_chart(Agg)
    st.write("### Economy vs Employment of Industry")
    st.plotly_chart(Ind)
    st.write("### Economy vs Employment of Services")
    st.plotly_chart(Ser)

# 🔴 creating 5th segment
    st.title("Trade")
    col = ['Exports', 'Imports', 'Balance']
    selected_col = st.selectbox('Select Column for Sorting', col)
    df = helper.Trade(Trade_df, selected_region, selected_col)
    st.table(df)


def Education_Technology_Page(df):
    edtech = prep.EducationandTechnology_preprocess(df)
    st.title("All Region Analysis")
    # 🔴 First Part Text 
    pm = edtech[edtech['Primary_m'] == edtech['Primary_m'].max()]['country'].values[0]
    pf = edtech[edtech['Primary_f'] == edtech['Primary_f'].max()]['country'].values[0]
    sm = edtech[edtech['Secondary_m'] == edtech['Secondary_m'].max()]['country'].values[0]
    sf = edtech[edtech['Secondary_f'] == edtech['Secondary_f'].max()]['country'].values[0]
    tm = edtech[edtech['Tertiary_m'] == edtech['Tertiary_m'].max()]['country'].values[0]
    tf = edtech[edtech['Tertiary_f'] == edtech['Tertiary_f'].max()]['country'].values[0]
    mob = edtech[edtech['Mobile'] == edtech['Mobile'].max()]['country'].values[0]
    In = edtech[edtech['Internet'] == edtech['Internet'].max()]['country'].values[0]

    st.write("## Top Country List in The World")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🔴 Primary Education")
        st.text(f" Male: {pm} \n Female: {pf}")
    with col2:
        st.write("### 🔴 Secondary Education")
        st.text(f" Male: {sm} \n Female: {sf}")

    col3, col4 = st.columns(2)
    with col1:
        st.write("### 🔴 Tertiary Education")
        st.text(f" Male: {tm} \n Female: {tf}")
    with col2:
        st.write("### 🔴 Technology ")
        st.text(f" Mobile: {mob} \n Internet: {In}")

    # First segment Pie charts
    mobile, internet = helper.Region_pi(edtech)
    st.write("#### Region wise Mobile Useage")
    st.plotly_chart(mobile)
    st.write("#### Region wise Internet Useage")
    st.plotly_chart(internet)

#🔴 Second segment 

    st.title('Region Specific Analysis')

    region = edtech['Region'].unique().tolist()
    selected_region = st.selectbox('Select a Region', region)

    edtech_r = edtech[edtech['Region']== selected_region]
    pmr = edtech_r[edtech['Primary_m'] == edtech_r['Primary_m'].max()]['country'].values[0]
    pfr = edtech_r[edtech['Primary_f'] == edtech_r['Primary_f'].max()]['country'].values[0]
    smr = edtech_r[edtech['Secondary_m'] == edtech_r['Secondary_m'].max()]['country'].values[0]
    sfr = edtech_r[edtech['Secondary_f'] == edtech_r['Secondary_f'].max()]['country'].values[0]
    tmr = edtech_r[edtech['Tertiary_m'] == edtech_r['Tertiary_m'].max()]['country'].values[0]
    tfr = edtech_r[edtech['Tertiary_f'] == edtech_r['Tertiary_f'].max()]['country'].values[0]
    mob = edtech_r[edtech_r['Mobile'] == edtech_r['Mobile'].max()]['country'].values[0]
    In = edtech_r[edtech_r['Internet'] == edtech_r['Internet'].max()]['country'].values[0]

    st.write(f"## Top Country List of {selected_region}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🔴 Primary Education")
        st.text(f" Male: {pmr} \n Female: {pfr}")
    with col2:
        st.write("### 🔴 Secondary Education")
        st.text(f" Male: {smr} \n Female: {sfr}")

    col3, col4 = st.columns(2)
    with col1:
        st.write("### 🔴 Tertiary Education")
        st.text(f" Male: {tmr} \n Female: {tfr}")
    with col2:
        st.write("### 🔴 Technology ")
        st.text(f" Mobile: {mob} \n Internet: {In}")

# 🔴 3rd Segment 
    options = ['Male', 'Female', 'Compare']
    gender = st.selectbox('Select stat topic', options)

    pr, sec, ter = helper.barplot(gender, edtech_r)
    st.title('Primary Education')
    st.plotly_chart(pr)
    st.title('Secondary Education')
    st.plotly_chart(sec)
    st.title('Tertiary Education')
    st.plotly_chart(ter)
