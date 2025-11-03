
# pip install finance_trading_ai_agents_mcp


# env variables:
### You can add environment variables in json format directly on the command line
### python -m finance_trading_ai_agents_mcp --env-config '{"DEBUG":"1","AITRADOS_SECRET_KEY":"sk-123..."}'
## windows:
```shell
@echo off
REM Windows batch file to run MCP with environment variables

echo Setting up environment variables...
set DEBUG=0
set ENABLE_RPC_PUBSUB_SERVICE=0
set AITRADOS_SECRET_KEY=YOUR_SECRET_KEY
#set OHLC_LIMIT_FOR_LLM=20
#set RENAME_COLUMN_NAME_MAPPING_FOR_LLM=interval:timeframe,
#set OHLC_COLUMN_NAMES_FOR_LLM=timeframe,close_datetime,open,high,low,close,volume

echo Starting MCP server...
echo ========================================
echo 🚀 Finance Trading AI Agents MCP Server
echo 📊 Debug Mode: %DEBUG%
echo 🔑 API Key: %AITRADOS_SECRET_KEY:~0,10%...
echo 📈 OHLC Limit: %OHLC_LIMIT_FOR_LLM%
echo ========================================

REM Run with default port (11435)
python -m finance_trading_ai_agents_mcp

pause
```
## linux
```shell
export DEBUG=0
export AITRADOS_SECRET_KEY="YOUR_SECRET_KEY"
#export ENABLE_RPC_PUBSUB_SERVICE=0
#export OHLC_LIMIT_FOR_LLM=20
#export RENAME_COLUMN_NAME_MAPPING_FOR_LLM="interval:timeframe,"
#export OHLC_COLUMN_NAMES_FOR_LLM="timeframe,close_datetime,open,high,low,close,volume"

```



# Use default port 11999


```shell
# auto finding .env file
python -m finance-trading-ai-agents-mcp #or finance-trading-ai-agents-mcp

#Specify .env file path
python -m finance_trading_ai_agents_mcp --env-file .env
```

```shell
python -m finance_trading_ai_agents_mcp --env-config {"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}

#or 

finance-trading-ai-agents-mcp --env-config {"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}
```

# Use --env-config
```shell
python -m finance_trading_ai_agents_mcp --env-config '{"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY","OHLC_LIMIT_FOR_LLM":"20","RENAME_COLUMN_NAME_MAPPING_FOR_LLM":"interval:timeframe,","OHLC_COLUMN_NAMES_FOR_LLM":"timeframe,close_datetime,open,high,low,close,volume","LIVE_STREAMING_OHLC_LIMIT":"150","ENABLE_RPC_PUBSUB_SERVICE":"1"}'


finance-trading-ai-agents-mcp --env-config '{"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY","OHLC_LIMIT_FOR_LLM":"20","RENAME_COLUMN_NAME_MAPPING_FOR_LLM":"interval:timeframe,","OHLC_COLUMN_NAMES_FOR_LLM":"timeframe,close_datetime,open,high,low,close,volume","LIVE_STREAMING_OHLC_LIMIT":"150"}'
```
# Specify port
```shell
python -m finance_trading_ai_agents_mcp -p 9000 --env-config '{"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}'
```
# Run with custom MCP server and custom MCP functions from Python file
```shell
python -m finance_trading_ai_agents_mcp -c examples/addition_custom_mcp_examples/addition_custom_mcp_example.py --env-config {"DEBUG":"1","AITRADOS_SECRET_KEY":"YOUR_SECRET_KEY"}

```