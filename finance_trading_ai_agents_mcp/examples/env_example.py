"""
######env file:

##debug
DEBUG=true

##Free Register at AiTrados website https://www.aitrados.com/ to get your API secret key (Free).
AITRADOS_SECRET_KEY=YOUR_SECRET_KEY

#MCP LLM Setting

##OHLC_LIMIT_FOR_LLM :Due to the window context size limitations of the Large Language Model (LLM), please set a reasonable number of OHLC rows. This setting will only affect the output to the LLM and will not influence strategy calculations
OHLC_LIMIT_FOR_LLM=20
##You can modify the ohlc column names to suit your trading system. Mapping example:name1:myname1,name2:myname2
RENAME_COLUMN_NAME_MAPPING_FOR_LLM=interval:timeframe,
##OHLC_COLUMN_NAMES_FOR_LLM:Filter out redundant column names for LLM input. The column names should be separated by commas.
OHLC_COLUMN_NAMES_FOR_LLM=timeframe,close_datetime,open,high,low,close,volume

"""
import os


def get_example_env():
    if not os.getenv('AITRADOS_SECRET_KEY'):
        os.environ['AITRADOS_SECRET_KEY'] = 'YOUR_SECRET_KEY' #Register at  https://www.aitrados.com/ to get your API secret key (Free).
        os.environ['DEBUG'] = 'true'
        os.environ['OHLC_LIMIT_FOR_LLM'] = '20'
        os.environ['RENAME_COLUMN_NAME_MAPPING_FOR_LLM'] = 'interval:timeframe,'
        os.environ['OHLC_COLUMN_NAMES_FOR_LLM'] = 'timeframe,close_datetime,open,high,low,close,volume'