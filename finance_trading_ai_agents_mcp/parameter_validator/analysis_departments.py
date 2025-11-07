from typing import Set, List, Dict, Any, Optional
import inspect

from finance_trading_ai_agents_mcp.mcp_services.traditional_indicator_operations.traditional_indicator_ops import \
    TraditionalIndicatorOps


class AnalysisDepartment:
    """
    Analysis Department Manager
    Supports dynamic addition and management of analysis departments
    """

    # Predefined core departments
    TRADITIONAL_INDICATOR = "traditional_indicator"
    PRICE_ACTION = "price_action"
    ECONOMIC_CALENDAR = "economic_calendar"
    #COMMODITY_FUNDAMENTAL = "commodity_fundamental"
    #STOCK_FUNDAMENTAL = "stock_fundamental"
    NEWS = "news"

    BROKER = "broker"
    MANAGER = "manager"
    DECISION_MAKER="decision_maker"

    def __init__(self):
        # Initialize core department set
        self._departments: Set[str] = {
            self.TRADITIONAL_INDICATOR,
            self.PRICE_ACTION,
            self.ECONOMIC_CALENDAR,
            self.NEWS,
            self.BROKER
            #self.COMMODITY_FUNDAMENTAL,
            #self.STOCK_FUNDAMENTAL,

            #self.MANAGER,
            #self.DECISION_MAKER
        }

        # Store metadata information for departments
        self._department_metadata: Dict[str, Dict[str, Any]] = {
            self.TRADITIONAL_INDICATOR: {
                "display_name": "Traditional Indicator",
            },
            self.PRICE_ACTION: {
                "display_name": "Price Action",
            },
            self.ECONOMIC_CALENDAR: {
                "display_name": "Economic Calendar",
            },

            self.NEWS: {
                "display_name": "News",
            },
            self.BROKER: {"display_name": "Broker"},

            #self.MANAGER: {"display_name": "Manager"},
            #self.DECISION_MAKER: {"display_name": "Decision_Maker"}

        }

    def add_department(self, name: str, display_name: Optional[str] = None) -> bool:
        """
        Add new analysis department

        Args:
            name: Department identifier (recommended to use lowercase letters and underscores)
            display_name: Display name

        Returns:
            bool: Returns True if added successfully, False if already exists
        """
        if name in self._departments:
            return False

        self._departments.add(name)

        # Add metadata
        self._department_metadata[name] = {
            "display_name": display_name or name.replace('_', ' ').title(),
        }

        # Dynamically add class attribute
        setattr(self.__class__, name.upper(), name)

        return True

    def get_all_departments(self) -> Set[str]:
        """Get all departments"""
        return self._departments.copy()

    def get_departments_list(self) -> List[str]:
        """Get department list (sorted)"""
        return sorted(list(self._departments))

    def get_department_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed department information"""
        if name not in self._departments:
            return None
        return self._department_metadata.get(name, {}).copy()

    def get_departments_by_category(self, category: str) -> List[str]:
        """Get departments by category"""
        return [
            name for name, meta in self._department_metadata.items()
            if meta.get("category") == category and name in self._departments
        ]

    def is_valid_department(self, name: str) -> bool:
        """Check if it's a valid department"""
        return name in self._departments

    def get_all_categories(self) -> Set[str]:
        """Get all categories"""
        return {
            meta.get("category", "unknown")
            for meta in self._department_metadata.values()
        }

    def get_departments_info(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information for all departments"""
        return {
            name: self._department_metadata.get(name, {})
            for name in self._departments
        }

    def get_class_constants(self) -> Dict[str, str]:
        """Get all constants (uppercase attributes) defined in the class"""
        constants = {}
        for name, value in inspect.getmembers(self.__class__):
            if (name.isupper() and
                    not name.startswith('_') and
                    isinstance(value, str) and
                    value in self._departments):
                constants[name] = value
        return constants

    def create_choices_for_validation(self) -> List[str]:
        """Create choice list for data validation"""
        return self.get_departments_list()

    def __contains__(self, item: str) -> bool:
        """Support 'in' operator"""
        return item in self._departments

    def __len__(self) -> int:
        """Support len() function"""
        return len(self._departments)

    def __iter__(self):
        """Support iteration"""
        return iter(sorted(self._departments))

    def __str__(self) -> str:
        """String representation"""
        return f"AnalysisDepartment({len(self._departments)} departments)"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"AnalysisDepartment(departments={self.get_departments_list()})"


# Create global instance
analysis_department = AnalysisDepartment()
