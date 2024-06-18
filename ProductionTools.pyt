
# Reloading of modules preformed here to make sure a toolbox refresh also
# reloads all associated modules. A refresh in ArcGIS Pro only reloads the code
# in this .pyt file, not the associated modules

from importlib import reload, invalidate_caches
invalidate_caches()

import utils.reloader
reload(utils.reloader)
from utils.reloader import import_tools

import utils.archelp
reload(utils.archelp)

import utils.tool
reload(utils.tool)

TOOLS = \
{
    "tools.prod":
        [
            "VertexBuffer",
        ],
    "tools.utility":
        [
            "VersionControl",
        ],
}

IMPORTS = import_tools(TOOLS)
globals().update({tool.__name__: tool for tool in IMPORTS})

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        
        self.label = "Production Tools"
        self.alias = self.label.replace(" ", "")
        
        # List of tool classes associated with this toolbox
        self.tools = IMPORTS