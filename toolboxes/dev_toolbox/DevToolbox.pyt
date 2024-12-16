import sys
import os
from pathlib import Path
from importlib import reload

# Manually add the path to the root of the project
ROOT = str(Path(__file__).parents[2].absolute())

# Insert the module roots to the system path
sys.path.insert(0, ROOT) # ../pytframe2
sys.path.insert(1, os.path.join(ROOT, "tools")) # ../pytframe2/tools
sys.path.insert(2, os.path.join(ROOT, "utils")) # ../pytframe2/utils
# NOTE: Add more module paths here if needed

# NOQA: E402, F401 Explanations
#   E402: sys path needs to be modified before importing modules
#       : This is beacause ArcPro uses this file as the entry point
#   
#   F401: Imports appear unused because they are used in the reloader
#       : This is because the reloader forces ArcPro to reload the modules
#       : If you don't do this, ArcPro will use the cached code preventing hot realoading

# Import dynamic modules with pyt_reload prefix
import utils.reloader as pyt_reload_reloader  # noqa: E402, F401
import utils.funcs.archelp as pyt_reload_archelp # noqa: E402, F401
import utils.tool as pyt_reload_tool # noqa: E402, F401

# Inline reloader of dynamic modules
[
    print(f"Reloaded {reload(module).__name__}") 
    for module_name, module in globals().items() 
    if module_name.startswith("pyt_reload")
]

# Import the Tool Importer function
from utils.reloader import import_tools # noqa: E402, F401
from utils.tool import Tool # noqa: E402, F401

## TODO: Move this to a configuration file
TOOLS =\
{
    "development":
        [
            "DevTool",
        ],
    "utilities":
        [
            "VersionControl",
        ],
    "production":
        [
            "VertexBuffer",
        ]
}

IMPORTS: list[type[Tool]] = import_tools(TOOLS)

# Manually add the tools to the global namespace
globals().update({tool.__name__: tool for tool in IMPORTS})

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        
        self.label = "Dev Toolbox"
        self.alias = "DevToolbox"
        
        # List of tool classes associated with this toolbox
        self.tools: list[type[Tool]] = IMPORTS