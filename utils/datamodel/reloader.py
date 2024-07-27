from importlib import reload, import_module
from traceback import format_exc
from utils.datamodel.tool import Tool

def placeholder_tool(tool_name: str, exception: Exception, traceback: str) -> type[Tool]:
    """ Higher order function for creating a tool class that represents a broken tool. """
    class _BrokenImport(Tool):
        __name__ = f"{tool_name}_BrokenImport"
        def __init__(self):
            self.category = "Broken Tools (Read Description for More Info)"
            self.label = f"{tool_name} - {exception}"
            self.alias = self.label.replace(" ", "")
            self.description = traceback
    return _BrokenImport

def get_module(module_name: str) -> type[Tool]:
    *_, tool = module_name.rsplit(".", 1)
    try:
        return getattr(reload(import_module(module_name)), tool)
    
    # Catch all exceptions beacuse the imported class can raise any exception
    # The placeholder makes this obvious in the ArcGIS Pro GUI and we write the
    # Traceback to the description of the _BrokenImport 'tool' for easy debugging
    except Exception as e:
        return placeholder_tool(tool, e, format_exc(limit=1))

def import_tools(tool_dict: dict[str, list[str]], tool_module_name: str = "tools") -> list[type[Tool]]:
    """ Import all tools from the provided dictionary.
    Default base module name is "tools".
    Expected format: {"module": ["tool1", "tool2", ...], ...}
    """
    return \
        [
            get_module(f'{tool_module_name}.{tool_sub_module}.{tool}')
            for tool_sub_module, tools in tool_dict.items()
            for tool in tools
        ]