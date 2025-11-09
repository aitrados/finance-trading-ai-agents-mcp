import datetime
import inspect
import os
import sys
import time
from pathlib import Path
from typing import List

from aitrados_api.common_lib.common import is_debug
from aitrados_api.common_lib.common_remote_curl import RemoteCurl
from aitrados_api.common_lib.tools.toml_manager import TomlManager

from fastmcp import Context

from aitrados_api.common_lib.contant import SchemaAsset, IntervalName

def get_content_from_file_or_url(file_or_url,headers=None):
    if isinstance(file_or_url,str) and (file_or_url.startswith("http://") or file_or_url.startswith("https://")):
        if  headers is None:
            headers = {"accept": "text/html"}
        res_data = RemoteCurl.get(file_or_url,headers,timeout=10)
        if "data" not in res_data:
            raise ValueError(f"Error remote url:{str(res_data)} ")
        return res_data["data"]

    if not isinstance(file_or_url,Path):
        file_or_url=Path(file_or_url)

    if not file_or_url.exists():
        raise  ValueError(f"File not found: {file_or_url}")
    try:
            content = file_or_url.read_text(encoding='utf-8')
            return content
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

def get_real_interval(interval:str):
    array=IntervalName.get_array()

    if not interval:
        raise ValueError(f"Invalid interval format. Expected '{array}'.")
    interval=interval.upper()
    if interval not in array:
        raise ValueError(f"Invalid interval format. Expected '{array}'.")
    return interval
def get_real_intervals(intervals:List[str]):
    new_intervals=[]
    array = IntervalName.get_array()
    if not intervals:
        raise ValueError(f"Invalid intervals format. Expected value in  '{array}'.")

    intervals=set(intervals)

    for  interval in intervals:
        new_intervals.append(get_real_interval(interval))
    return new_intervals


def split_full_symbol(full_symbol:str):
    if not isinstance(full_symbol, str) or full_symbol.count(':') < 2:
        raise ValueError(f"Invalid full_symbol ({full_symbol}) format. Expected 'ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL'.")
    full_symbol=full_symbol.upper()
    asset_name, country_symbol = full_symbol.split(':', 1)
    if asset_name.lower() not in SchemaAsset.get_array():
        raise ValueError(f"Invalid asset name: '{asset_name}' of '{full_symbol}'. Expected one of {SchemaAsset.get_array()}.")
    return asset_name, country_symbol

def get_fixed_full_symbol(full_symbol:str):
    asset_name, country_symbol=split_full_symbol(full_symbol)
    standard_full_symbol_key = f"{asset_name}:{country_symbol}"
    return standard_full_symbol_key



def mcp_get_api_params(context: Context,params:dict)->dict:
    secret_key = context.request_context.request.headers.get("secret_key",None)
    example_mcp_config={
  "mcpServers": {
    "xxxxx": {
      "url": "http://xxxxx/xxxxx/",
      "transport": "streamable-http",
      "headers": {
        "SECRET_KEY": "your-secret-key"
      }
    }
  }
}
    if not secret_key:
        raise ValueError(f'Missing secret_key from MCP config head.Example:{example_mcp_config}.Please stop all tasks and  tell him to improve the parameters')

    if os.getenv("AITRADOS_SECRET_KEY", "SET_YOUR_SECRET_KEY")!=secret_key:
        raise ValueError(f'secret_key is not correct from MCP config head.Example:{example_mcp_config}.Please stop all tasks and  tell him to improve the parameters')



    return params



def generate_custom_mcp_template(output_path: str = "my_custom_mcp.py"):
    """
    Generate custom MCP template file
    Copy content from example file and personalize it

    Args:
        output_path: Output file path
    """
    try:
        file_path = Path(output_path)

        if file_path.exists():
            print(f"⚠️  File already exists: {file_path}")
            response = input("Do you want to overwrite? (y/N): ")
            if response.lower() != 'y':
                print("❌ Template generation cancelled")
                return

        # Get example file path
        current_dir = Path(__file__).parent
        example_file_path = current_dir / "examples" / "addition_custom_mcp_examples" / "addition_custom_mcp_example.py"

        if not example_file_path.exists():
            print(f"❌ Example file not found: {example_file_path}")

            # Try other possible paths
            alternative_paths = [
                current_dir.parent / "examples" / "addition_custom_mcp_examples" / "addition_custom_mcp_example.py",
                Path("finance_trading_ai_agents_mcp") / "examples" / "addition_custom_mcp_examples" / "addition_custom_mcp_example.py",
                Path("examples") / "addition_custom_mcp_examples" / "addition_custom_mcp_example.py"
            ]

            for alt_path in alternative_paths:
                if alt_path.exists():
                    example_file_path = alt_path
                    print(f"🔍 Found example file: {example_file_path}")
                    break
            else:
                print("🔍 Please check if the example file path is correct")
                return

        # Read example file content
        with open(example_file_path, 'r', encoding='utf-8') as source_file:
            template_content = source_file.read()

        # Personalization: Replace class name
        output_filename = Path(output_path).stem
        class_name = ''.join(word.capitalize() for word in output_filename.replace('_', ' ').replace('-', ' ').split())

        # Replace example class name with user-defined class name
        if "AdditionCustomMcpExample" in template_content:
            template_content = template_content.replace(
                "class AdditionCustomMcpExample",
                f"class {class_name}CustomMcp"
            )

        # Add custom header comment
        custom_header = f'''"""
Custom MCP Implementation File
Filename: {output_path}
Generated at: {Path(__file__).stat().st_mtime}

This file is generated based on the example template. You can:
1. Modify class names and method implementations
2. Add new tool methods
3. Customize business logic

Usage:
finance_trading_ai_agents_mcp generate -c {output_path}
"""

'''

        # Add custom header at the beginning of the file
        template_content = custom_header + template_content

        # Write to target file
        with open(file_path, 'w', encoding='utf-8') as target_file:
            target_file.write(template_content)

        print(f"✅ Successfully generated custom MCP template: {file_path}")
        print(f"📄 Template based on example file: {example_file_path}")
        print(f"🔧 Auto-generated class name: {class_name}CustomMcp")
        print("📝 Please edit this file to implement your custom MCP functionality")
        print(f"🚀 Usage: aitrados-mcp-server -c {file_path}")
        print(f"🔍 You can also check the running example: run_mcp_server_with_addition_custom_mcp_file_example.py")

    except Exception as e:
        print(f"❌ Template generation failed: {e}")
        import traceback
        traceback.print_exc()


def show_mcp_result(mcp,result,is_exception=False):
    if is_debug():
        if is_exception:
            icon="❌"
        else:
            icon="🎉"

        print(icon * 20, mcp.name,"->", inspect.currentframe().f_back.f_code.co_name, "-" * 20, datetime.datetime.now())
        print(result)
        print(icon * 10, mcp.name,"end", "-" * 10)




def show_environment_info(host, port,addition_custom_mcp_py_file):
     # Start server
     print("=" * 60)
     print("🚀 Finance Trading AI Agents MCP Server")
     print("=" * 60)
     print(f"🌐 Server Address: http://{host}:{port}")
     # print(f"📡 WebSocket: ws://{args.host}:{args.port}")
     if addition_custom_mcp_py_file:
         print(f"📂 Custom MCP: {addition_custom_mcp_py_file}")
     print("=" * 60)
     print("📋 Environment Variables:")

     # Show current environment variables (mask sensitive ones)
     env_vars = ['DEBUG', 'AITRADOS_SECRET_KEY', 'ENABLE_RPC_PUBSUB_SERVICE', 'OHLC_LIMIT_FOR_LLM',
                 'RENAME_COLUMN_NAME_MAPPING_FOR_LLM', 'OHLC_COLUMN_NAMES_FOR_LLM',
                 'LIVE_STREAMING_OHLC_LIMIT']

     for var in env_vars:
         value = os.getenv(var, 'Not Set')
         if 'SECRET' in var or 'KEY' in var:
             if value != 'Not Set':
                 masked_value = value[:10] + '...' if len(value) > 10 else '***'
                 print(f"   🔑 {var}: {masked_value}")
             else:
                 print(f"   🔑 {var}: {value}")
         else:
             print(f"   ⚙️  {var}: {value}")
     if not TomlManager.c:
        print(f"   ⚙️  Toml file loaded : Not yet")
     else:
        print(f"   ⚙️  Toml file loaded : Yes")



     print("=" * 60)
     print("Press Ctrl+C to stop the server")
     print()