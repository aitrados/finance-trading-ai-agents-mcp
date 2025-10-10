import importlib.util
import os
import sys
from pathlib import Path
from typing import Optional

from aitrados_api.common_lib.common import is_debug
from loguru import logger


def add_addition_custom_mcp(addition_custom_mcp_py_file: Optional[str] = None):
    """
    Dynamically load user-defined MCP file
    Supports custom files that import other user modules

    Args:
        addition_custom_mcp_py_file: Path to user-defined MCP Python file
    """
    if not addition_custom_mcp_py_file:
        if is_debug():
            logger.debug("No custom MCP file specified, skipping")
        return

    try:
        # Convert to Path object, supporting both relative and absolute paths
        file_path = Path(addition_custom_mcp_py_file).resolve()

        if not file_path.exists():
            logger.error(f"❌ Custom MCP file does not exist: {file_path}")
            exit()

        if not file_path.suffix == '.py':
            logger.error(f"❌ Custom MCP file must be a Python file (.py): {file_path}")
            exit()

        if is_debug():
            logger.debug(f"🔄 Loading custom MCP file: {file_path}")

        # 🔧 Important: Add the user file's directory to Python path
        # This allows user files to import other modules from the same directory or subdirectories
        user_file_dir = file_path.parent
        original_sys_path = sys.path.copy()  # Backup original path

        if str(user_file_dir) not in sys.path:
            sys.path.insert(0, str(user_file_dir))
            if is_debug():
                logger.debug(f"🔧 Added user directory to Python path: {user_file_dir}")


        current_dir = user_file_dir
        for _ in range(3):  # Search up to 3 directory levels
            parent_dir = current_dir.parent
            if parent_dir != current_dir and str(parent_dir) not in sys.path:
                # Check if parent directory contains Python files or __init__.py, suggesting it's a Python project root
                if any(parent_dir.glob("*.py")) or (parent_dir / "__init__.py").exists():
                    sys.path.insert(0, str(parent_dir))
                    if is_debug():
                        logger.debug(f"🔧 Added parent directory to Python path: {parent_dir}")
            current_dir = parent_dir

        original_cwd = os.getcwd()
        try:
            os.chdir(user_file_dir)
            if is_debug():
                logger.debug(f"🔧 Changed working directory to: {user_file_dir}")

            # Create module specification
            module_name = f"custom_mcp_{file_path.stem}_{hash(str(file_path)) % 10000}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)

            if spec is None or spec.loader is None:
                logger.error(f"❌ Unable to create module specification: {file_path}")
                exit()

            # Create module
            custom_module = importlib.util.module_from_spec(spec)


            custom_module.__file__ = str(file_path)
            if hasattr(custom_module, '__path__'):
                custom_module.__path__ = [str(user_file_dir)]

            # Add to sys.modules
            sys.modules[module_name] = custom_module

            # Execute module
            spec.loader.exec_module(custom_module)

            if is_debug():
                logger.debug(f"✅ Successfully loaded custom MCP file: {file_path}")

            # Find and instantiate all classes that inherit from AdditionCustomMcpInterface
            _instantiate_custom_mcp_classes(custom_module, file_path)

        finally:

            os.chdir(original_cwd)
            if is_debug():
                logger.debug(f"🔧 Restored working directory to: {original_cwd}")

    except ImportError as e:
        logger.error(f"❌ Import error in custom MCP file: {e}")
        logger.error("💡 Tip: Make sure all imported modules are in the same directory or subdirectories")
        logger.error(f"💡 Tip: Current file location: {file_path}")
        logger.error(f"💡 Tip: Working directory: {os.getcwd()}")
        logger.error(
            f"💡 Tip: Python path includes: {[p for p in sys.path if 'custom' in p or str(file_path.parent) in p]}")
        import traceback
        traceback.print_exc()
        exit()
    except Exception as e:
        logger.error(f"❌ Failed to load custom MCP file: {e}")
        import traceback
        traceback.print_exc()
        exit()
    finally:
        pass


def _instantiate_custom_mcp_classes(module, file_path: Path = None):
    """
    Find and instantiate all classes in the module that inherit from AdditionCustomMcpInterface

    Args:
        module: The loaded module
        file_path: Path to the original file (for better error reporting)
    """
    from finance_trading_ai_agents_mcp.addition_custom_mcp.addition_custom_mcp_interface import \
        AdditionCustomMcpInterface

    instantiated_count = 0

    for name in dir(module):
        obj = getattr(module, name)

        # Check if it's a class that inherits from AdditionCustomMcpInterface
        if (isinstance(obj, type) and
                issubclass(obj, AdditionCustomMcpInterface) and
                obj is not AdditionCustomMcpInterface):

            try:
                # Instantiate class
                instance = obj()
                logger.info(f"✅ Successfully instantiated custom MCP class: {name}")
                instantiated_count += 1
            except Exception as e:
                logger.error(f"❌ Failed to instantiate custom MCP class {name}: {e}")
                if file_path:
                    logger.error(f"💡 Error in file: {file_path}")
                import traceback
                traceback.print_exc()

    if instantiated_count == 0:
        logger.error("⚠️  No classes inheriting from AdditionCustomMcpInterface found in custom MCP file")
        if file_path:
            logger.error(f"💡 File checked: {file_path}")
            logger.error("💡 Make sure your class inherits from AdditionCustomMcpInterface")
            logger.error("💡 Example: class MyCustomMcp(AdditionCustomMcpInterface):")
        exit()
    else:
        logger.info(f"🎉 Total instantiated {instantiated_count} custom MCP classes")