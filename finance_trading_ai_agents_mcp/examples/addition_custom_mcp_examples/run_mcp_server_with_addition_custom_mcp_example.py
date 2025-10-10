from finance_trading_ai_agents_mcp import mcp_run

from finance_trading_ai_agents_mcp.examples.env_example import get_example_env

if __name__ == "__main__":
    get_example_env()
    from finance_trading_ai_agents_mcp.examples.addition_custom_mcp_examples.addition_custom_mcp_example import \
        AdditionCustomMcpExample
    AdditionCustomMcpExample()
    mcp_run()