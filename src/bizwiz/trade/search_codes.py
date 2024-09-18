"""Hamilton drivers for obtaining search info"""
import pathlib
import pandas as pd

from hamilton import driver

from . import dags

def find_country_codes(
    keywords:list[str],
    filepath : str | pathlib.Path,
)->pd.DataFrame:
    #validate
    filepath = pathlib.Path(filepath)
    if filepath.exists() is False:
        raise FileNotFoundError(f"File not found: {filepath}")
    
    filepath = str(filepath.resolve())
    
    
    #build graph
    dr =  driver.Builder().with_modules(dags.find_country_data).build()

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