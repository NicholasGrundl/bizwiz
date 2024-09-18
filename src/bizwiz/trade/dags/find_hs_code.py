"""Find HS Code(s) from keyword"""
from typing_extensions import Annotated

import pandas as pd
from pydantic import BaseModel, Field, StringConstraints
import openai
import instructor
from hamilton.function_modifiers import tag

from ... import trade_data

VariableName = Annotated[
    str, 
    StringConstraints(to_lower=True, pattern=r"[a-z][_a-z0-9]*")
]


class RankedResult(BaseModel):
    id: str = Field(description="The HS Code as a string")
    score: int = Field(description="The fuzzy search score of the result")
    text: str = Field(description="The text of the result")
    rank : int = Field(description="The ordinal rank of the result, 1 is the best")
    reasoning: str = Field(description="The reasoning behind the rank")
    chemical_name: VariableName = Field(description="common chemical name")

@tag(cache="parquet")
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

    Choose the best and most appropriate HS Code given the search.
    """

    return llm_prompt

def rank_search(api_key:str | None, rank_prompt:str, model: str = "gpt-4o-mini")->RankedResult:
    llm_client = instructor.from_openai(openai.OpenAI(api_key=api_key))


    messages = [{"role": "user","content": rank_prompt,}]
    #generate the new question
    response = llm_client.chat.completions.create(
        model=model,
        response_model=RankedResult,
        messages=messages,
    )
    return response
