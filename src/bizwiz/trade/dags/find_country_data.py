"""Find country from keyword"""
import pandas as pd

import comtradeapicall as comtrade
from ... import trade_data


def country_codes(filepath:str)->pd.DataFrame:
    df = pd.read_csv(filepath)
    df['iso'] = df['alpha-3']

    ordered_cols = [
        'name','iso'
    ]
    unordered_cols = df.columns.difference(ordered_cols).tolist()
    return df[ordered_cols+unordered_cols].copy()

def country_search(
    keyword:str, 
    country_codes:pd.DataFrame,
    limit:int=5, 
    score_threshold:int=85,
)->pd.DataFrame:
    """Find country iso code from keyword"""
    df = trade_data.fuzzy_search_df(
        query=keyword, 
        df=country_codes, 
        id_column='iso', 
        search_column='name', 
        limit=limit, 
        score_threshold=score_threshold,
    )
    return df

def country_data(country_search:pd.DataFrame)->dict:
    df = country_search.copy()
    #rank search
    if df.shape[0]==0:
        return {}
    elif df.shape[0]==1:
        # found a best hit
        info = df.iloc[0].to_dict()
    else:
        #rank and choose best hit
        info = df.sort_values(by=['score'], ascending=False).iloc[0].to_dict()
    #grab comtrade code
    comtrade_query = comtrade.convertCountryIso3ToCode(info['iso'])
    
    country_data = {
        'name' : info['name'],
        'iso' : info['iso'],
        'comtrade_query' : comtrade_query,
    }

    return country_data
