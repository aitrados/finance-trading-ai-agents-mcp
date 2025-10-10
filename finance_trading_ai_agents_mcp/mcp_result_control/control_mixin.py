from abc import ABC

from aitrados_api.common_lib.any_list_data_to_format_data import AnyListDataToFormatData
from aitrados_api.common_lib.contant import ApiDataFormat
from aitrados_api.common_lib.response_format import UnifiedResponse, ErrorResponse




class ControlMixin(ABC):
    def __init__(self,api_result: UnifiedResponse | ErrorResponse):
        self.api_result = api_result
        self.mcp_result=None
        if isinstance(api_result,ErrorResponse):
            raise ValueError(f"Error:{api_result.message},detail:{api_result.detail}")


        self.empty_data_result=None

        self.data_type=None
    def set_common_list_result(self):
        if self.mcp_result:
            return self

        result=self.api_result.result
        if not result:
            raise ValueError("The pulled data is empty")
            return self


        if "count" not in result:
            self.mcp_result=result
            return self

        if result["count"]==0:
            raise ValueError("The pulled data list is empty" if not self.empty_data_result else self.empty_data_result)

        self.mcp_result=result["data"]
        return self

    def set_common_dict_result(self):
        if self.mcp_result:
            return self

        result=self.api_result.result
        if not result:
            raise ValueError("The pulled data is empty" if not self.empty_data_result else self.empty_data_result)

        self.mcp_result = result
        return self
    def result(self,data_type="list",empty_data_result=None):
        self.data_type=data_type
        if empty_data_result:
            self.empty_data_result=empty_data_result


        if data_type=="list":

            self.set_common_list_result()
        else:
            self.set_common_dict_result()
        return self
    def to_list_data(self,rename_column_name_mapping=None,filter_column_names=None,limit=None,format: str = ApiDataFormat.CSV):
        to_format = AnyListDataToFormatData(self.mcp_result,
                                            rename_column_name_mapping=rename_column_name_mapping,
                                            filter_column_names=filter_column_names, limit=limit)
        if format.lower()==ApiDataFormat.CSV:
            return to_format.get_csv()

        if format.lower()==ApiDataFormat.JSON:
            return to_format.get_list()










