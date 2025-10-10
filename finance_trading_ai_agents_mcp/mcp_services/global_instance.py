import os
from typing import List

from fastmcp import FastMCP

from finance_trading_ai_agents_mcp.utils.common_utils import get_env_value

default_ohlc_limit = get_env_value("OHLC_LIMIT_FOR_LLM", 150)

def get_rename_column_name_mapping():
    string = os.getenv("RENAME_COLUMN_NAME_MAPPING_FOR_LLM",
                                None)
    if not string:
        return None
    mapping={}
    string = string.strip(",")
    keys_array = str.split(string, ",")

    for key_ in keys_array:
        try:
            key,value=str.split(string, ":")
            mapping[key]=value
        except:
            pass
    if not mapping:
        mapping=None
    return mapping


def get_filter_column_names():
    column_name_str = os.getenv("OHLC_COLUMN_NAMES_FOR_LLM", "datetime,close_datetime,open,high,low,close,volume")
    column_name_str = column_name_str.strip(",")
    keys_array = str.split(column_name_str, ",")
    return keys_array
rename_column_name_mapping=get_rename_column_name_mapping()
filter_column_names=get_filter_column_names()



class CustomMcpServer:
    def __init__(self):
        self.mcp_list:List[FastMCP]=[]
        self._mcp_apps=[]

    def add_mcp_server(self,mcp:FastMCP):
        if not isinstance(mcp,FastMCP):
            return
        self.mcp_list.append( mcp)



custom_mcp_server=CustomMcpServer()

