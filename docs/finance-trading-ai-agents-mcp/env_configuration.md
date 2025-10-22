---
weight: 1100
date: "2025-09-03T22:37:22+01:00"
draft: false
author: "VON"
title: "Environment Configuration"
icon: "settings"
toc: true
description: "Complete guide for configuring environment variables and settings for the MCP trading system"
publishdate: "2025-09-12T22:37:22+01:00"
tags: ["Environment Setup", "Configuration", "API Keys", "MCP Server", "Trading System", "Environment Variables", "Setup Guide"]
categories: ["Configuration", "Setup"]
keywords: ["environment variables", "configuration", "setup", "API keys", "trading system"]
---

```dotenv
##debug
DEBUG=true


##Free Register at AiTrados website https://www.aitrados.com/ to get your API secret key (Free).
AITRADOS_SECRET_KEY=YOUR_SECRET_KEY

##Enable RPC/PubSub Service.you can cross process/software/code language communication.easily call api /websocks/other service
ENABLE_RPC_PUBSUB_SERVICE=0

##LIVE_STREAMING_OHLC_LIMIT:Real-time OHLC data stream length,default 150
##Prevent the strategy result from not being obtained due to insufficient ohlc length. For example, the value of MA200 can only be calculated when the length of ohlc is greater than 200.
#LIVE_STREAMING_OHLC_LIMIT=150

#MCP LLM Setting

##OHLC_LIMIT_FOR_LLM :Due to the window context size limitations of the Large Language Model (LLM), please set a reasonable number of OHLC rows. This setting will only affect the output to the LLM and will not influence strategy calculations
##If it is a multi-period chart analysis, the OHLC_LIMIT_FOR_LLM adjustment is smaller
OHLC_LIMIT_FOR_LLM=30
##You can modify the ohlc column names to suit your trading system. Mapping example:name1:myname1,name2:myname2
RENAME_COLUMN_NAME_MAPPING_FOR_LLM=interval:timeframe,
##OHLC_COLUMN_NAMES_FOR_LLM:Filter out redundant column names for LLM input. The column names should be separated by commas.
OHLC_COLUMN_NAMES_FOR_LLM=timeframe,close_datetime,open,high,low,close,volume

```

```python
import os


def get_example_env():
    if not os.getenv('AITRADOS_SECRET_KEY'):
        os.environ['AITRADOS_SECRET_KEY'] = 'YOUR_SECRET_KEY' #Register at  https://www.aitrados.com/ to get your API secret key (Free).
        os.environ['DEBUG'] = 'true'
        os.environ['ENABLE_RPC_PUBSUB_SERVICE'] = 'true'

        os.environ['OHLC_LIMIT_FOR_LLM'] = '20'
        os.environ['RENAME_COLUMN_NAME_MAPPING_FOR_LLM'] = 'interval:timeframe,'
        os.environ['OHLC_COLUMN_NAMES_FOR_LLM'] = 'timeframe,close_datetime,open,high,low,close,volume'
```