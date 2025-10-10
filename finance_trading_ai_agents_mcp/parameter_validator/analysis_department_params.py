from typing import Annotated, List, Any, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict
from finance_trading_ai_agents_mcp.parameter_validator.analysis_departments import analysis_department



class CompanyDepartmentParams(BaseModel):
    """Parameters supporting multiple department selection"""

    # Pydantic V2 configuration
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "departments": ["news", "economic_calendar", "traditional_indicator"]
            }
        }
    )

    departments: Annotated[
        List[str],
        Field(
            description="List of selected departments, multiple departments can be combined",
            min_length=1,
            json_schema_extra={
                "example": ["news", "economic_calendar", "traditional_indicator"]
            }
        )
    ]

    @field_validator('departments')
    @classmethod
    def validate_departments_complete(cls, v: List[str]) -> List[str]:
        """Complete department validation including validity check and deduplication"""
        if not v:
            raise ValueError('At least one department must be selected')

        # Check for duplicates
        if len(v) != len(set(v)):
            duplicates = [item for item in set(v) if v.count(item) > 1]
            raise ValueError(f'Duplicate departments are not allowed: {duplicates}')

        # Validate the validity of each department
        invalid_departments = []
        for dept in v:
            if not analysis_department.is_valid_department(dept):
                invalid_departments.append(dept)

        if invalid_departments:
            available = analysis_department.get_departments_list()
            raise ValueError(
                f'Invalid departments: {invalid_departments}. '
                f'Available departments: {available}'
            )

        return v

    @classmethod
    def get_available_departments(cls) -> List[str]:
        """Get list of all available departments"""
        return analysis_department.get_departments_list()

    @classmethod
    def get_departments_by_category(cls, category: str) -> List[str]:
        """Get departments by category"""
        return analysis_department.get_departments_by_category(category)

    @classmethod
    def get_schema_with_current_departments(cls) -> Dict[str, Any]:
        """Get schema including currently available departments"""
        # Use Pydantic V2 method
        schema = cls.model_json_schema()
        available_departments = analysis_department.get_departments_list()

        # Update description to include available departments
        if 'properties' in schema and 'departments' in schema['properties']:
            schema['properties']['departments']['description'] = (
                f"List of selected departments, available options: {', '.join(available_departments)}"
            )
            # Use examples instead of example in V2
            schema['properties']['departments']['examples'] = [available_departments[:3]]

        # Update global examples
        schema['examples'] = [{
            "departments": available_departments[:3]
        }]

        return schema

    @classmethod
    def create_dynamic_schema(cls) -> Dict[str, Any]:
        """Create dynamic schema containing information about all current departments"""
        available_departments = analysis_department.get_departments_list()
        departments_info = analysis_department.get_departments_info()
        categories = analysis_department.get_all_categories()

        return {
            "available_departments": available_departments,
            "departments_info": departments_info,
            "categories": list(categories),
            "schema": cls.model_json_schema(),
            "examples": [
                {"departments": ["news", "economic_calendar"]},
                {"departments": ["traditional_indicator", "price_action"]},
                {"departments": available_departments[:3]}
            ]
        }

    def get_department_details(self) -> Dict[str, Any]:
        """Get detailed information about currently selected departments"""
        return {
            dept: analysis_department.get_department_info(dept)
            for dept in self.departments
        }

    def get_selected_categories(self) -> List[str]:
        """Get all categories of currently selected departments"""
        categories = set()
        for dept in self.departments:
            info = analysis_department.get_department_info(dept)
            if info and 'category' in info:
                categories.add(info['category'])
        return list(categories)

'''
# Export analysis department class for backward compatibility

__all__ = ['CompanyDepartmentParams', 'AnalysisDepartment']

# Usage examples and tests
if __name__ == "__main__":
    print("=== CompanyDepartmentParams Test ===")

    # Test valid parameters
    try:
        valid_params = CompanyDepartmentParams(
            departments=["news", "economic_calendar", "traditional_indicator"]
        )
        print("✅ Valid parameters created successfully:")
        print(f"   Selected departments: {valid_params.departments}")
        print(f"   Department details: {valid_params.get_department_details()}")
        print(f"   Categories involved: {valid_params.get_selected_categories()}")

    except Exception as e:
        print(f"❌ Valid parameter test failed: {e}")

    # Test invalid parameters
    try:
        invalid_params = CompanyDepartmentParams(
            departments=["invalid_dept", "news"]
        )
        print(f"❌ This should not succeed: {invalid_params.departments}")
    except Exception as e:
        print(f"✅ Correctly caught invalid departments: {e}")

    # Test duplicate departments
    try:
        duplicate_params = CompanyDepartmentParams(
            departments=["news", "news", "economic_calendar"]
        )
        print(f"❌ This should not succeed: {duplicate_params.departments}")
    except Exception as e:
        print(f"✅ Correctly caught duplicate departments: {e}")

    # Test empty list
    try:
        empty_params = CompanyDepartmentParams(departments=[])
        print(f"❌ This should not succeed: {empty_params.departments}")
    except Exception as e:
        print(f"✅ Correctly caught empty list: {e}")

    # Show available information
    print(f"\n=== Available Information ===")
    print(f"All available departments: {CompanyDepartmentParams.get_available_departments()}")

    for category in analysis_department.get_all_categories():
        depts = CompanyDepartmentParams.get_departments_by_category(category)
        if depts:
            print(f"{category} category departments: {depts}")

    # Show dynamic schema
    print(f"\n=== Dynamic Schema Information ===")
    dynamic_schema = CompanyDepartmentParams.create_dynamic_schema()
    print(f"Number of available departments: {len(dynamic_schema['available_departments'])}")
    print(f"Number of categories: {len(dynamic_schema['categories'])}")
    print(f"Example: {dynamic_schema['examples'][0]}")
'''