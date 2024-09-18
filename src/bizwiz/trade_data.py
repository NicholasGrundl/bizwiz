"""Obtaining trade data"""


import pandas as pd
import requests
import comtradeapicall as comtrade



import csv
from typing import List, Tuple
from fuzzywuzzy import process



#### Find country codes
def load_country_data(file_path: str) -> List[Tuple[str, str, str]]:
    """
    Load country data from a CSV file.
    
    :param file_path: Path to the CSV file containing country data
    :return: List of tuples containing (country name, alpha-2 code, alpha-3 code)
    """
    countries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            countries.append((row[0], row[1], row[2]))
    return countries

def fuzzy_search_country(
    query: str, 
    countries: List[Tuple[str, str, str]], 
    limit: int = 5
) -> List[Tuple[str, str, str, int]]:
    """
    Perform a fuzzy search on country names and return matching countries with their ISO codes.
    
    :param query: Search query string
    :param countries: List of country data tuples
    :param limit: Maximum number of results to return
    :return: List of tuples containing (country name, alpha-2 code, alpha-3 code, match score)
    """
    country_names = [country[0] for country in countries]
    matches = process.extract(query, country_names, limit=limit)
    
    results = []
    for match in matches:
        country_name, score = match
        index = country_names.index(country_name)
        country_data = countries[index]
        results.append((*country_data, score))
    
    return results

def search_country_iso(keyword:str, countries : List[Tuple[str, str, str]],)->pd.DataFrame:
    results = fuzzy_search_country(keyword, countries)
    df = pd.DataFrame(data=results, columns = ['name','alpha-2','alpha-3','score'],)
    df['iso'] = df['alpha-3']
    return df[['name','iso','score']].copy()


##### Find available data

def get_available_df(subscription_key:str,com_country:int):
    df = comtrade.getFinalDataAvailability(
        subscription_key,
        typeCode='C',freqCode='M',clCode='HS',
        reporterCode=com_country,
        period=None
    )
    df['date'] = pd.to_datetime(df['period'], format='%Y%m')
    return df

def filter_df_date(df, start_date, end_date, date_column='date'):
    """
    Filter a pandas DataFrame to include only rows where the date_column
    is between start_date and end_date (inclusive).

    date format 'YYYY-MM-DD'
    """
    # Convert string dates to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Ensure the date column is in datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Filter the DataFrame
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    return df.loc[mask].copy()


####### Find commodity codes
def get_references_df()->pd.DataFrame:
    # List available reference data
    references = comtrade.listReference()
    return references

def get_hs_commodities_df(hs_versions=None):
    #TODO: make this a dict and find by HS version names
    available_versions = ['cmd:HS','cmd:H0','cmd:H1','cmd:H2','cmd:H3','cmd:H4','cmd:H5','cmd:H6']
    
    # List available HS commodities
    references = get_references_df()

    if hs_versions is None:
        hs_versions = ['cmd:HS']
    
    # Find the URL for HS classification
    cmd_references = references[references['category'].isin(hs_versions)]
    cmd_uris = cmd_references['fileuri'].tolist()
    hs_df = pd.DataFrame()
    for uri in cmd_uris:
        # print(f"fetching {uri}")
        r = requests.get(uri)
        data = r.json()
        _df = pd.DataFrame.from_records(data['results'])
        hs_df = pd.concat([hs_df, _df])
    hs_df = hs_df.reset_index(drop=True)
    # print("completed data retrieval")
    # print(f"- # Codes: {hs_df.shape[0]}")
    # print(f"- Columns: {hs_df.columns.tolist()}")
    return hs_df


# Search for codes
def fuzzy_search_df(query, df, id_column, search_column, limit=5, score_threshold=60):
    """
    Perform a fuzzy search on a DataFrame column.
    
    Args:
    query (str): The search query.
    df (pd.DataFrame): The DataFrame to search.
    id_column (str): The name of the column to use as the ID.
    search_column (str): The name of the column to search in.
    limit (int): The maximum number of results to return. Default is 5.
    score_threshold (int): The minimum score for a result to be included. Default is 60.
    
    Returns:
    pd.DataFrame: A DataFrame of search results.
    """
    
    # Perform the fuzzy search
    results = process.extractBests(query, df[search_column], limit=len(df), score_cutoff=score_threshold)
    
    # Create a DataFrame from the results
    result_df = pd.DataFrame(results, columns=[search_column, 'score', 'index'])
    
    # Add the ID column
    result_df[id_column] = df.loc[result_df['index'], id_column].values
    
    # Sort by score descending and limit the results
    result_df = result_df.sort_values('score', ascending=False).head(limit)
    
    # Reorder columns
    result_df = result_df[[id_column, search_column, 'score']]
    
    return result_df


# TODO: duplicates in the above, look into this more later
# TODO: implement a fuzze search of the above to get codes
# - use an llm hs_df['text'].sample(n=10).to_list()


###### Get data for a country, commodity, year pair
def get_available_periods(
    com_country:list, 
    hs_code:str,
    year:str | int, 
    api_key:str,
)->list[str]:
    
    #computed
    start_date=f"{year}-01-01"
    end_date=f"{year}-12-31"

    if len(com_country)==1:
        com_country_query = com_country[0]
    else:
        com_country_query = ",".join([str(v) for v in com_country])
    
    # Query the data
    available_df = get_available_df(subscription_key=api_key, com_country=com_country_query)
    available_df = filter_df_date(available_df, start_date, end_date, date_column='date')
    available_periods = available_df['period'].tolist()
    return available_periods


def get_trade_data(
    com_country:list, 
    hs_code:str,
    periods:list[int], 
    api_key:str,
    kind='import'
):
    available_flow_codes = {
        'import' : 'M',
        'export' : 'X',
    }
    if kind not in available_flow_codes.keys():
        raise ValueError(f"kind must be one of {list(available_flow_codes.keys())}")
    else:
        flow_code = available_flow_codes.get(kind)

    if len(com_country)==1:
        com_country_query = str(com_country[0])
    else:
        com_country_query = ",".join([str(v) for v in com_country])
    
    periods_query = ",".join([str(v) for v in periods])
    flow = 'M' # 'M' for Import 'X' for Export

    df = comtrade.getFinalData(
        subscription_key=api_key, 
        typeCode='C', freqCode='M', clCode='HS',
        period=periods_query,
        reporterCode=com_country_query,
        cmdCode=hs_code, flowCode=flow_code, 
        partnerCode=None, #world/ all partners
        partner2Code=None, customsCode=None,motCode=None,
        maxRecords=None,format_output='JSON',
        breakdownMode='classic', includeDesc=True,
    )
    
    return df


def process_trade_data(
    df:pd.DataFrame, 
)->pd.DataFrame:
    processed_df = df.copy()
    processed_df = processed_df[~processed_df.isna()]

    #time metrics
    processed_df['date'] = pd.to_datetime(processed_df['period'], format='%Y%m')

    #price data
    processed_df['value'] = processed_df['primaryValue']
    processed_df['mass'] = processed_df['netWgt']
    processed_df['price'] = processed_df['value']/processed_df['mass']
    #drop price out of bounds/bad data
    processed_df = processed_df[processed_df['price'].between(0,9999999)].copy()

    #countries
    processed_df['iso'] = processed_df['reporterISO']
    processed_df['partner'] = processed_df['partnerISO']

    #qtyunits
    processed_df['qty'] = processed_df['qty']
    processed_df['qty_units'] = processed_df['qtyUnitAbbr']
    processed_df['qty_unit_code'] = processed_df['qtyUnitCode']

    #order columns
    ordered_columms = [
        'date','iso','partner','price','mass','value','qty','qty_units','qty_unit_code'
    ]
    unordered_columns = processed_df.columns.difference(ordered_columms).tolist()
    return processed_df[ordered_columms+unordered_columns].copy()

def remove_unkown_partners(df:pd.DataFrame, country_df:pd.DataFrame)->pd.DataFrame:
    processed_df = pd.merge(left=df, right=country_df, left_on=['iso'], right_on=['iso'])
    processed_df = processed_df[processed_df['partner'].isin(country_df['iso'].tolist())]
    return processed_df.copy()


def get_trade_metrics(
    import_df, 
    export_df, 
    premium_frac=0.1, 
    transport_distance=100, 
    transport_price=0.15
):
    metrics = {}
    metrics['value_units'] = '$' 
    metrics['mass_units'] = 'kg'
    
    # Total Trade Metrics
    metrics['mass_import'] = import_df['mass'].sum()
    metrics['mass_export'] = export_df['mass'].sum()
    metrics['mass_total'] = metrics['mass_import'] + metrics['mass_export']
    metrics['fraction_import'] = metrics['mass_import'] / metrics['mass_total']
    
    metrics['value_import'] = import_df['value'].sum()
    metrics['value_export'] = export_df['value'].sum()
    metrics['value_total'] = metrics['value_import'] + metrics['value_export']
    
    # Total price
    if metrics['mass_total'] > 0:
        metrics['price_total'] = metrics['value_total'] / metrics['mass_total']
    else:
        metrics['price_total'] = 0

    # Kind (import, export, or balanced)
    if metrics['mass_total'] > 0:
        import_fraction = metrics['fraction_import']
        if import_fraction > 0.9:
            metrics['kind'] = 'import'
        elif import_fraction < 0.1:
            metrics['kind'] = 'export'
        else:
            metrics['kind'] = 'balanced'
    else:
        metrics['kind'] = '-'

    # Premium calculation
    premium_frac = 0.1  # Assuming a 10% premium, adjust as needed
    metrics['value_premium'] = metrics['price_total'] * premium_frac

    # Transport calculations
    transport_distance = 100  # km (assumption)
    transport_price = 0.15  # $/t*km
    metrics['value_transport'] = transport_price * transport_distance
    
    return metrics


import matplotlib.pyplot as plt
def get_annotated_scatter(
    df, 
    x_col, y_col, 
    color_col, key_col, 
    title=''
):
    """
    Create a scatter plot from a pandas DataFrame.
    
    Args:
    df (pd.DataFrame): The DataFrame containing the data.
    x_col (str): The column name for the x-axis.
    y_col (str): The column name for the y-axis.
    color_col (str): The column name for the color of points.
    key_col (str): The column name for the labels of points.
    title (str): The title of the plot (default: 'Scatter Plot').
    
    Returns:
    None. Displays the plot.
    """
    
    # Create the scatter plot
    fig, ax = plt.subplots(1,1, figsize=(12, 8))
    plt.close()
    colors = {
        'import' : 'blue',
        'export' : 'red',
        'balanced' : 'green',
    }
    
    for groups, group_df in df.groupby(by=['kind']):
        color = colors.get(groups[0])
        ax.scatter(group_df[x_col], group_df[y_col], color=color, label=groups[0])
    
    # Add labels and title
    ax.set(xlabel=x_col, ylabel=y_col, title=title)
    
    # Add labels for each point
    for i, txt in enumerate(df[key_col]):
        ax.annotate(
            txt, 
            (df[x_col].iloc[i], df[y_col].iloc[i]), 
            xytext=(5,5), 
            textcoords='offset points', 
            fontsize=8
        )
    ax.legend()
    # Adjust layout and display the plot
    return fig