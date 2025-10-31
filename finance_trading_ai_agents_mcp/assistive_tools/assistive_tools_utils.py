from finance_trading_ai_agents_mcp.mcp_services.global_instance import McpGlobalVar
from finance_trading_ai_agents_mcp.utils.common_utils import get_content_from_file_or_url
from finance_trading_ai_agents_mcp.utils.contant import SystemPromptLanguage
from pathlib import Path
from aitrados_api.common_lib.common_remote_curl import RemoteCurl

def get_basic_system_function_call_prompt(lang='en',file_or_url:str=None,header=None):
    if lang not in SystemPromptLanguage.get_array():
        lang = "en"
    if not file_or_url:
        base_dir = Path(__file__).parent / "basic_system_function_call_prompt_words"
        file_or_url = base_dir / f"{lang}.md"
    content = get_content_from_file_or_url(file_or_url, header)
    if isinstance(content,str):
        content=content.replace("{live_streaming_ohlc_limit}",str(McpGlobalVar.live_streaming_ohlc_limit()))
    return content





def get_client_mcp_config(departments: list[str],mcp_base_url=None) -> dict:
    """
    '''
    mcp_config={
      "mcpServers": {
        "news": {
          "url": "http://127.0.0.1:11999/news/",
          "transport": "streamable-http",
          "headers": {
            "SECRET_KEY": "xxx"
          }
        }
      }
    }
    '''
    """
    if not mcp_base_url:
        mcp_base_url="http://127.0.0.1:11999"

    url=mcp_base_url+"/mcp.json"
    try:
        mcp_config = RemoteCurl.post(url, {"departments": departments})
        if not isinstance( mcp_config,dict) or "data" not in mcp_config:
            raise KeyError(mcp_config)
        return mcp_config["data"]
    except Exception as e:
        raise KeyError(f"Error requesting MCP configuration: {e}")
