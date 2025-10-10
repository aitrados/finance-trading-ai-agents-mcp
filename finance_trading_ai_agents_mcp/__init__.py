"""
Aitrados Finance Multiple AI Agents MCP

A specialized MCP server for financial analysis and quantitative trading.
"""

__version__ = "0.0.1"
__author__ = "Alexander"
__email__ = "support@aitrados.com"





from .addition_custom_mcp.addition_custom_mcp_interface import AdditionCustomMcpInterface

from .parameter_validator.analysis_departments import analysis_department
from .mcp_manage import mcp_run




from .utils.common_remote_curl import RemoteCurl




__all__ = [
    'analysis_department',

    'mcp_run',
    'AdditionCustomMcpInterface',

]