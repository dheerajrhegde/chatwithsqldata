import openai, os
import pandas as pd
from pandas import DataFrame

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase

openai.api_key = os.getenv("OPENAI_API_KEY")

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy import create_engine

mysql_uri = 'mysql+mysqlconnector://root:bittu2012@localhost:3306/Chinook'
db = SQLDatabase.from_uri(mysql_uri)
engine = sa.create_engine(mysql_uri, echo=True)

def is_delete(df):
    for i in range(len(df)):
        if df.iloc[i]["select_type"] == "DELETE":
            return True
    return False

def is_update(df):
    for i in range(len(df)):
        if df.iloc[i]["select_type"] == "UPDATE":
            return True
    return False

def too_many_rows(df):
    for i in range(len(df)):
        if int(df.iloc[i]["rows"]) > 500 :
            return True
    return False

def execute(query, query_type):
    if query_type == 'explain':
        with engine.connect() as conn:
           result = conn.execute(text("EXPLAIN "+query))
           df = pd.DataFrame(result.all(), columns=result.keys())
    if query_type == 'query':
        with engine.connect() as conn:
           result = conn.execute(text(query))
           df = pd.DataFrame(result.all(), columns=result.keys())
    return df

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)

def run_full_pipeline(question: str)->DataFrame:
    sql_query = chain.invoke({"question": question})
    sql_query = sql_query.replace("\n", " ")
    df = execute(sql_query, "explain")
    if is_delete(df): return ("Delete not allowed",df)
    if is_update(df): return ("Update not allowed", df)
    if too_many_rows(df): return ("More than 500 rows selected from each table", df)
    df = execute(sql_query, "query")
    return ("query executed", df)
