import pandas as pd
import comtradeapicall as comtrade
from hamilton.function_modifiers import tag

from ... import trade_data



#inputs
def comtrade_country(country_code : str = 'USA')->str:
    return comtrade.convertCountryIso3ToCode(country_code)

def comtrade_year(year : str | int = 2024)->str:
    return str(year)

#workflow
@tag(cache="parquet")
def available_df(
    comtrade_country : str,
    api_key : str, # Move this to ENV var
    comtrade_year : str,
)->pd.DataFrame:
    
    comtrade_query = comtrade.convertCountryIso3ToCode(comtrade_country)

    #find available periods for country
    available_df = trade_data.get_available_df(subscription_key=api_key, com_country=comtrade_query)
    
    start_date=f"{comtrade_year}-01-01"
    end_date=f"{comtrade_year}-12-31"

    available_df = trade_data.filter_df_date(available_df, start_date, end_date, date_column='date')

    return available_df
