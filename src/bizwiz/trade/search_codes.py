"""Hamilton drivers for obtaining search info"""
import pathlib
import pandas as pd

from hamilton import driver

from ..llm import load_llm_env
from .dags import find_country_data, find_hs_code


def get_country_codes(
    keywords:list[str],
    filepath : str | pathlib.Path,
)->pd.DataFrame:
    #validate
    filepath = pathlib.Path(filepath)
    if filepath.exists() is False:
        raise FileNotFoundError(f"File not found: {filepath}")
    
    filepath = str(filepath.resolve())
    
    
    #build graph
    dr =  driver.Builder().with_modules(find_country_data).build()

    #execute
    final_vars = ["country_data"]
    inputs = {
        'keyword' : '',
        'filepath' : filepath,
    }

    data=[]
    for keyword in keywords:
        overrides = {'keyword' : keyword}

        #execute
        results = dr.execute(
            final_vars=final_vars,
            inputs=inputs,
            overrides=overrides,
        )
        data.append({
            **results['country_data'],
            'keyword' : keyword,
        })
            
    return pd.DataFrame(data=data)


def get_hs_codes(
    keywords:list[str],
    api_key : str | None = None,
)->pd.DataFrame:
    """Search for HS codes and use an llm to rank them"""
    #using llm
    if api_key is None:
        load_llm_env()

    #build graph
    dr =  driver.Builder().with_modules(find_hs_code).build()
    
    #execute
    final_vars = ["rank_search"]
    inputs = {
        'keyword' : '',
        'chemical_formula' : None,
        'api_key' : api_key,
    }

    data=[]
    for keyword in keywords:
        overrides =  {'keyword' : keyword}
        results = dr.execute(
            final_vars=final_vars,
            inputs=inputs,
            overrides=overrides,
        )
        best_hs_code = results['rank_search'].model_dump()
        data.append({
            **best_hs_code,
            'keyword' : keyword,
        })

    return pd.DataFrame(data=data)