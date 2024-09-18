"""Hamilton drivers for obtaining trade data by period"""

from hamilton import driver

from .dags import find_available_data, find_trade_data


def get_trade_data(
    api_key : str,
    hs_codes : list[str],
    country_code : str = 'USA',
    year : int = 2024,
)->list[dict]:
    
    ##### Check what data is available for country in year
    dr =  driver.Builder().with_modules(find_available_data).build()
    #execute
    inputs = {  
        'country_code' : country_code,
        'year' : year,
        'api_key' : api_key,
    }
    results = dr.execute(
        final_vars=["available_df"],
        inputs=inputs,
        overrides={},
    )
    available_df = results['available_df'].copy()
    if available_df.empty:
        #No trade data available for that year
        return []


    ##### Grab data for each hs code code
    trade_data = []
    for hs_code in hs_codes:
        data = {
            'hs_code' : hs_code,
        }

        dr =  driver.Builder().with_modules(find_trade_data).build()
        
        #execute
        inputs = {  
            'country_code' : country_code,
            'hs_code' : hs_code,
            'available_df' : available_df,
            'api_key' : api_key,
        }

        results = dr.execute(
            final_vars=["processed_data"],
            inputs=inputs,
            overrides={'kind' : 'import',},
        )
        df = results['processed_data']
        df['kind'] = 'import'
        data['import'] = df.copy()

        results = dr.execute(
            final_vars=["processed_data"],
            inputs=inputs,
            overrides={'kind' : 'export',},
        )
        df = results['processed_data']
        df['kind'] = 'export'
        data['export'] = df.copy()
        trade_data.append(data)
    return trade_data
