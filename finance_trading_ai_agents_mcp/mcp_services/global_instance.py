import os
from typing import List
from aitrados_api.common_lib.common import get_env_value
from fastmcp import FastMCP
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
    column_name_str = os.getenv("OHLC_COLUMN_NAMES_FOR_LLM", "datetime,close_datetime,interval,open,high,low,close,volume")
    column_name_str = column_name_str.strip(",")
    keys_array = str.split(column_name_str, ",")
    return keys_array



class McpGlobalVar:
    __default_ohlc_limit=None
    __rename_column_name_mapping=None
    __filter_column_names=None
    __live_streaming_ohlc_limit=None


    @classmethod
    def rename_column_name_mapping(cls):
        if cls.__rename_column_name_mapping is None:
            cls.__rename_column_name_mapping=get_rename_column_name_mapping()
        return cls.__rename_column_name_mapping


    @classmethod
    def filter_column_names(cls):
        if cls.__filter_column_names is None:
            cls.__filter_column_names=get_filter_column_names()
        return cls.__filter_column_names


    @classmethod
    def default_ohlc_limit(cls):
        if cls.__default_ohlc_limit is None:
            cls.__default_ohlc_limit=get_env_value("OHLC_LIMIT_FOR_LLM", 150)
        return cls.__default_ohlc_limit
    @classmethod
    def live_streaming_ohlc_limit(cls):
        if cls.__live_streaming_ohlc_limit is None:
            cls.__live_streaming_ohlc_limit=get_env_value("LIVE_STREAMING_OHLC_LIMIT", 150)
        return cls.__live_streaming_ohlc_limit





class CustomMcpServer:
    mcp_list: List[FastMCP] = []
    _mcp_apps = []


    @classmethod
    def add_mcp_server(cls,mcp:FastMCP):
        if not isinstance(mcp,FastMCP):
            return
        cls.mcp_list.append( mcp)



#custom_mcp_server=CustomMcpServer()

