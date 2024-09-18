"""Find HS Code(s) from keyword"""
import pandas as pd

import comtradeapicall as comtrade
from ... import trade_data



def hs_codes()->pd.DataFrame:
    # List available reference data
    df = trade_data.get_hs_commodities_df(hs_versions=None)
    return df


def chemical_context(chemical_formula:str | None)->str:
    """search external database for chemical information"""
    if chemical_formula is None:
        return ''
    
    context = f"The chemical formula is {chemical_formula}"
    return context

def keyword_search(
    keyword:str, 
    hs_codes:pd.DataFrame,
    limit:int=5, 
    score_threshold:int=85,
)->pd.DataFrame:
    df = trade_data.fuzzy_search_df(
        query=keyword, 
        df=hs_codes, 
        id_column='id', 
        search_column='text',  
        limit=limit, 
        score_threshold=score_threshold,
    )
    return df

def keyword_context(keyword_search:pd.DataFrame)->str:
    
    context = keyword_search.to_json()
    return context



def rank_prompt(keyword:str, keyword_context:str, chemical_context:str)->str:
    """Use an llm to rank the results"""
    
    llm_prompt = f"""
    The user is searching for an appropriate HS Code to represent a specific chemical.

    We ran have multiple search hits and need to rank them to find the best candidate.

    # Search Information

    Below is information about our current search

    ## User Input
    {keyword}

    ## Keyword Results
    {keyword_context}

    ## Additional Chemical Information
    {chemical_context}
  
    # Instructions

    Rank the Keyword results ordinally starting with 1 as the best and most appropriate HS Code for the search.
    """

    return llm_prompt

