
"""Command line interface for aitrados-finance-multiple-ai-agents-mcp"""
import argparse
import sys
import json
import os

from aitrados_api.common_lib.common import load_env_file


from .utils.common_utils import generate_custom_mcp_template



def set_env_from_json(json_config):
    """
    Set environment variables from JSON configuration

    Args:
        json_config: JSON string or dict containing environment variables
    """
    if isinstance(json_config, str):
        try:
            config = json.loads(json_config)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in env-config: {e}")
    elif isinstance(json_config, dict):
        config = json_config
    else:
        raise ValueError("env-config must be a JSON string or dictionary")

    if not isinstance(config, dict):
        raise ValueError("env-config JSON must be an object/dictionary")

    print("📝 Setting environment variables from JSON config:")
    for key, value in config.items():
        if not isinstance(key, str):
            raise ValueError(f"Environment variable key must be string, got {type(key)}: {key}")

        # Convert value to string for environment variables
        str_value = str(value)
        os.environ[key] = str_value

        # Mask sensitive information in output
        if 'SECRET' in key.upper() or 'KEY' in key.upper() or 'TOKEN' in key.upper():
            masked_value = str_value[:10] + '...' if len(str_value) > 10 else '***'
            print(f"   🔑 {key}: {masked_value}")
        else:
            print(f"   ⚙️  {key}: {str_value}")


def load_env_from_file(file_path):
    """
    Load environment variables from JSON file

    Args:
        file_path: Path to JSON configuration file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise ValueError(f"Environment config file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Error reading config file {file_path}: {e}")


def mcp_cli_command():
    """Entry point for the MCP server command line interface."""
    parser = argparse.ArgumentParser(
        description='Start MCP (Model Context Protocol) Server',
        prog='aitrados-mcp-server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic usage
  python -m finance_trading_ai_agents_mcp

  # With custom port
  python -m finance_trading_ai_agents_mcp -p 9000

  # With environment variables from JSON string
  python -m finance_trading_ai_agents_mcp --env-config '{"DEBUG":"1","AITRADOS_SECRET_KEY":"sk-123..."}'

  # With environment variables from JSON file
  python -m finance_trading_ai_agents_mcp --env-config-file config.json
  python -m finance_trading_ai_agents_mcp --env-file .env

  # Complete example with all options
  python -m finance_trading_ai_agents_mcp -p 8000 --host 0.0.0.0 -c custom.py --env-config '{"DEBUG":"1"}'

JSON Config Example:
  {
    "DEBUG": "1",
    "AITRADOS_SECRET_KEY": "YOUR_SECRET_KEY",
    "ENABLE_RPC_PUBSUB_SERVICE": "1",
    "OHLC_LIMIT_FOR_LLM": "20",
    "RENAME_COLUMN_NAME_MAPPING_FOR_LLM": "interval:timeframe,",
    "OHLC_COLUMN_NAMES_FOR_LLM": "timeframe,close_datetime,open,high,low,close,volume",
    "LIVE_STREAMING_OHLC_LIMIT": "150"
  }
        '''
    )

    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Server start command (default)
    server_parser = subparsers.add_parser('serve', help='Start MCP server')
    server_parser.add_argument('-p', '--port', type=int, default=11999,
                               help='Port to run the server on (default: 11999)')
    server_parser.add_argument('--host', type=str, default='127.0.0.1',
                               help='Host to bind the server to (default: 127.0.0.1)')
    server_parser.add_argument('-c', '--custom-mcp', type=str, dest='custom_mcp_file',
                               help='Path to custom MCP Python file')
    server_parser.add_argument('--env-config', type=str,
                               help='JSON string containing environment variables')
    server_parser.add_argument('--env-config-file', type=str,
                               help='Path to JSON file containing environment variables')
    server_parser.add_argument('--env-file', type=str,
                               help='Path to env file containing environment variables')

    # Generate template command
    template_parser = subparsers.add_parser('generate', help='Generate custom MCP template')
    template_parser.add_argument('-o', '--output', type=str, default='my_custom_mcp.py',
                                 help='Output file path (default: my_custom_mcp.py)')

    # Version information
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.3')

    # Compatibility with old parameter format (default to serve when no subcommand)
    parser.add_argument('-p', '--port', type=int, default=11999, help='Port to run the server on (default: 11999)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind the server to (default: 127.0.0.1)')
    parser.add_argument('-c', '--custom-mcp', type=str, dest='custom_mcp_file', help='Path to custom MCP Python file')
    parser.add_argument('--env-config', type=str,
                        help='JSON string containing environment variables')
    parser.add_argument('--env-config-file', type=str,
                        help='Path to JSON file containing environment variables')
    parser.add_argument('--env-file', type=str,
                        help='Path to env file containing environment variables')

    args = parser.parse_args()

    try:
        # Handle environment configuration first
        if args.env_config and args.env_config_file:
            raise ValueError("Cannot use both --env-config and --env-config-file at the same time")

        if args.env_config:
            set_env_from_json(args.env_config)
        elif args.env_config_file:
            config = load_env_from_file(args.env_config_file)
            set_env_from_json(config)
        elif args.env_file:
            load_env_file(args.env_file,override=True)



        # Handle subcommands
        if args.command == 'generate':
            generate_custom_mcp_template(args.output)
            return
        elif args.command == 'serve' or args.command is None:

            from .mcp_manage import mcp_run
            mcp_run(
                port=args.port,
                host=args.host,
                addition_custom_mcp_py_file=args.custom_mcp_file
            )
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)