"""
Entry point for running the package as a module.
Usage: python -m finance_trading_ai_agents_mcp [options]
"""

from .mcp_cli import mcp_cli_command

if __name__ == "__main__":
    mcp_cli_command()