'''
Title: Dataframe Preprocessor
Description : Take dataframe and create a custom data fame according to the need of application
'''

import re

def extract_migrant_no(x):
    
    pattern = r'(\d+\.\d+)'
    match = re.search(pattern, x)
    return match.group(1)


def Overalldf_preprocess(Overalldf):
    Overalldf = Overalldf[['country','Region','Population in thousands (2017)','International migrant stock (000/% of total pop.)', 'GDP: Gross domestic product (million current US$)', 'Seats held by women in national parliaments %', 'Threatened species (number)' ]]
    Overalldf['Total Migrants'] = Overalldf['International migrant stock (000/% of total pop.)'].apply(extract_migrant_no)
    Overalldf.drop(columns=['International migrant stock (000/% of total pop.)'], inplace=True)
    column_name_mapping = {
    'Population in thousands (2017)': 'Population(Thousand)',
    'GDP: Gross domestic product (million current US$)': 'GDP',
    'Seats held by women in national parliaments %': 'Women in Parliament(%)',
    'Threatened species (number)':'Threatened species',
    }

    Overalldf.rename(columns=column_name_mapping, inplace=True)

    return Overalldf


def RegionalEconomy_preprocess(df):
    #break down into sub data frames
    GDP_df = df[['country',
             'Region',
             'GDP: Gross domestic product (million current US$)',
             'GDP growth rate (annual %, const. 2005 prices)',
             'GDP per capita (current US$)']]

    Economy_df = df[['country',
                 'Region',
                 'Economy: Agriculture (% of GVA)',
                 'Economy: Industry (% of GVA)',
                 'Economy: Services and other activity (% of GVA)']]

    Employment_df = df[['country',
                    'Region',
                    'Employment: Agriculture (% of employed)',
                    'Employment: Industry (% of employed)',
                    'Employment: Services (% of employed)']]

    Trade_df = df[['country',
               'Region',
               'International trade: Exports (million US$)',
               'International trade: Imports (million US$)',
               'International trade: Balance (million US$)']]

    extra_df = df[['country',
               'Region',
               'Health: Total expenditure (% of GDP)',
               'Education: Government expenditure (% of GDP)']]
    
    #Renaming Columns
    GDP_name_mapping = {
        'GDP: Gross domestic product (million current US$)': 'GDP',
        'GDP growth rate (annual %, const. 2005 prices)': 'GDP growth',
        'GDP per capita (current US$)': 'GDP/capita',
    }

    Economy_name_mapping = {
        'Economy: Agriculture (% of GVA)': 'Agriculture',
        'Economy: Industry (% of GVA)': 'Industry',
        'Economy: Services and other activity (% of GVA)':'Services',
    }

    Employment_name_mapping = {
        'Employment: Agriculture (% of employed)': 'emp_Agriculture',
        'Employment: Industry (% of employed)':'emp_Industry',
        'Employment: Services (% of employed)': 'emp_Services',
    }

    Trade_name_mapping = {
        'International trade: Exports (million US$)': 'Exports',
        'International trade: Imports (million US$)': 'Imports',
        'International trade: Balance (million US$)': 'Balance',
    }

    extra_name_mapping = {
        'Health: Total expenditure (% of GDP)': 'Health',
        'Education: Government expenditure (% of GDP)': 'Education',
    }

    GDP_df.rename(columns=GDP_name_mapping, inplace=True)
    Economy_df.rename(columns=Economy_name_mapping, inplace=True)
    Employment_df.rename(columns=Employment_name_mapping, inplace=True)
    Trade_df.rename(columns=Trade_name_mapping, inplace=True)
    extra_df.rename(columns=extra_name_mapping, inplace=True)

    # Removing rows with wrong value

    Economy_df['Agriculture'] = Economy_df['Agriculture'].astype('float')
    Economy_df['Induatry'] = Economy_df['Industry'].astype('float')
    Economy_df['Services'] = Economy_df['Services'].astype('float')

    Trade_df['Exports']= Trade_df['Exports'].astype('int')
    Trade_df['Imports']= Trade_df['Imports'].astype('int')
    Trade_df['Balance']= Trade_df['Balance'].astype('int')

    Employment_df['emp_Agriculture'] = Employment_df['emp_Agriculture'].astype('float')
    Employment_df['emp_Industry'] = Employment_df['emp_Industry'].astype('float')
    Employment_df['emp_Services'] = Employment_df['emp_Services'].astype('float')

    return GDP_df, Economy_df, Employment_df, Trade_df, extra_df


def EducationandTechnology_preprocess(df):
    edtech = df[['country', 'Region','Education: Primary gross enrol. ratio (f/m per 100 pop.)', 'Education: Secondary gross enrol. ratio (f/m per 100 pop.)', 'Education: Tertiary gross enrol. ratio (f/m per 100 pop.)', 'Mobile-cellular subscriptions (per 100 inhabitants)', 'Individuals using the Internet (per 100 inhabitants)']]
    mapping = {
    'Education: Primary gross enrol. ratio (f/m per 100 pop.)': 'Primary',
    'Education: Secondary gross enrol. ratio (f/m per 100 pop.)':'Secondary',
    'Education: Tertiary gross enrol. ratio (f/m per 100 pop.)': 'Tertiary',
    'Mobile-cellular subscriptions (per 100 inhabitants)':'Mobile',
    'Individuals using the Internet (per 100 inhabitants)': 'Internet',   
    }

    edtech.rename(columns=mapping, inplace=True)
    edtech['Primary_f'] = edtech['Primary'].apply(lambda x: re.search(r"(\d+\.\d+)\/", x).group(1))
    edtech['Primary_m'] = edtech['Primary'].apply(lambda x: re.search(r'\/(\d+)', x).group(1))

    edtech['Secondary_f'] = edtech['Secondary'].apply(lambda x: re.search(r"(\d+\.\d+)\/", x).group(1))
    edtech['Secondary_m'] = edtech['Secondary'].apply(lambda x: re.search(r'\/(\d+)', x).group(1))

    edtech['Tertiary_f'] = edtech['Tertiary'].apply(lambda x: re.search(r"(\d+\.\d+)\/", x).group(1))
    edtech['Tertiary_m'] = edtech['Tertiary'].apply(lambda x: re.search(r'\/(\d+)', x).group(1))

    edtech.drop(columns=['Primary','Secondary','Tertiary'], inplace=True)
    return edtech

