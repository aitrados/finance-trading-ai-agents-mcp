
from pathlib import Path
from aitrados_api.common_lib.common import get_env_value
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import PlainTextResponse, HTMLResponse

from finance_trading_ai_agents_mcp.parameter_validator.analysis_department_params import CompanyDepartmentParams
from finance_trading_ai_agents_mcp.parameter_validator.analysis_departments import analysis_department


def set_mcp_config(app: FastAPI):


    @app.post("/mcp.json")
    def get_mcp_config(request: Request, params: CompanyDepartmentParams):

        base_url = f"{request.url.scheme}://{request.url.netloc}"


        selected_departments = [dept for dept in params.departments]

        mcp_list = {}
        for mcp_type in selected_departments:
            mcp_config = {
                "url": f"{base_url}/{mcp_type}/",
                "transport": "streamable-http",
                "headers": {"SECRET_KEY": get_env_value("AITRADOS_SECRET_KEY", "YOUR_AITRADOS_SECRET_KEY")},
            }
            mcp_list[mcp_type] = mcp_config

        data = {"mcpServers": mcp_list}
        return data
    @app.get("/mcp_servers.json")
    def get_mcp_servers(request: Request):

        base_url = f"{request.url.scheme}://{request.url.netloc}"


        selected_departments = analysis_department.get_departments_list()

        mcp_list = {}
        for mcp_type in selected_departments:
            mcp_config = {
                "url": f"{base_url}/{mcp_type}/",
                "transport": "streamable-http",
                "headers": {"SECRET_KEY": get_env_value("AITRADOS_SECRET_KEY", "YOUR_AITRADOS_SECRET_KEY")},
            }
            mcp_list[mcp_type] = mcp_config

        data = {"mcpServers": mcp_list}
        return data

    @app.get("/", response_class=HTMLResponse)
    def get_root(request: Request):
        base_url = f"{request.url.scheme}://{request.url.netloc}"

        # 尝试读取HTML文件
        current_file_dir = Path(__file__).parent
        html_path = current_file_dir / "index.html"

        html_content = html_path.read_text(encoding='utf-8')
        html_content = html_content.replace('{base_url}', base_url)
        html_content = html_content.replace('{departments}', ', '.join(analysis_department.get_departments_list()))


        return HTMLResponse(content=html_content)


