import pandas as pd
import comtradeapicall as comtrade

from ... import trade_data


#inputs
def comtrade_country(country_code : str = 'USA')->str:
    return comtrade.convertCountryIso3ToCode(country_code)

def comtrade_flow(kind : str = 'import')->str:
    if kind=='import':
            return 'M'
    elif kind=='export':
            return 'X'
    #default to import
    return 'M'


#workflow
def periods(available_df:pd.DataFrame)->list[str]:
    """return the list of unique periods"""
    periods = available_df['period'].unique().tolist()
    return [
        str(v) 
        for v in periods
    ]

def comtrade_periods(periods: list[str],)->str:
     return ",".join([str(v) for v in periods])

def comtrade_hs_code(hs_code : str | int,)->str:
     return str(hs_code)
     

def query_parameters(
    comtrade_country : str,
    comtrade_periods: str, 
    comtrade_flow : str,
    comtrade_hs_code: str,
    api_key : str,
)->dict[str,str]:
    query = {
        'subscription_key' : api_key, 
        'typeCode':'C', 
        'freqCode':'M',
        'clCode':'HS',
        'period':comtrade_periods,
        'reporterCode':comtrade_country,
        'cmdCode': comtrade_hs_code,
        'flowCode':comtrade_flow,
        'partnerCode':None,#world/ all partners
        'partner2Code':None,
        'customsCode':None,
        'motCode':None,
        'maxRecords':None,
        'format_output':'JSON',
        'breakdownMode':'classic',
        'includeDesc':True,
    }
    return query

def raw_trade_data(
    query_parameters : dict[str,str],
)->pd.DataFrame:
    df = comtrade.getFinalData(**query_parameters)
    return df


def processed_data(
    raw_trade_data : pd.DataFrame,
)->pd.DataFrame:
    df = raw_trade_data.copy()
    df = df[~df.isna()]

    #if empty send back empty
    if df.empty:
        #REFACTOR, verbose for now to catch error in near term
        comtrade_columns = [
            'typeCode',
            'freqCode',
            'refPeriodId',
            'refYear',
            'refMonth',
            'period',
            'reporterCode',
            'reporterISO',
            'reporterDesc',
            'flowCode',
            'flowDesc',
            'partnerCode',
            'partnerISO',
            'partnerDesc',
            'partner2Code',
            'partner2ISO',
            'partner2Desc',
            'classificationCode',
            'classificationSearchCode',
            'isOriginalClassification',
            'cmdCode',
            'cmdDesc',
            'aggrLevel',
            'isLeaf',
            'customsCode',
            'customsDesc',
            'mosCode',
            'motCode',
            'motDesc',
            'qtyUnitCode',
            'qtyUnitAbbr',
            'qty',
            'isQtyEstimated',
            'altQtyUnitCode',
            'altQtyUnitAbbr',
            'altQty',
            'isAltQtyEstimated',
            'netWgt',
            'isNetWgtEstimated',
            'grossWgt',
            'isGrossWgtEstimated',
            'cifvalue',
            'fobvalue',
            'primaryValue',
            'legacyEstimationFlag',
            'isReported',
            'isAggregate'
        ]
        #order columns
        ordered_columms = [
            'date','iso','partner','price','mass','value','qty','qty_units','qty_unit_code'
        ]
        df = pd.DataFrame(data=[], columns = ordered_columms + comtrade_columns)
        unordered_columns = df.columns.difference(ordered_columms).tolist()
        return df[ordered_columms+unordered_columns].copy()

    #time metrics
    df['date'] = pd.to_datetime(df['period'], format='%Y%m')

    #price data
    df['value'] = df['primaryValue']
    df['mass'] = df['netWgt']
    df['price'] = df['value']/df['mass']
    
    #countries
    df['iso'] = df['reporterISO']
    df['partner'] = df['partnerISO']

    #qtyunits
    df['qty'] = df['qty']
    df['qty_units'] = df['qtyUnitAbbr']
    df['qty_unit_code'] = df['qtyUnitCode']

    # #fitler based on content
    df = df[df['price'].between(0,9999999)].copy()
    
    #order columns
    ordered_columms = [
        'date','iso','partner','price','mass','value','qty','qty_units','qty_unit_code'
    ]
    unordered_columns = df.columns.difference(ordered_columms).tolist()
    return df[ordered_columms+unordered_columns].copy()

