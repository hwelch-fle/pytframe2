import arcpy
import subprocess
import os

from utils.tool import Tool
from utils import archelp
from utils import models

class VersionControl(Tool):
    WORKDIR = os.path.join(os.path.dirname(__file__), "..")
    BRANCHES = \
        subprocess.run(
            ["git", "branch", "-a"], 
            cwd=WORKDIR, 
            capture_output=True,
            text=True,
            shell=True,
        ).stdout.strip().replace('*','').strip().split("\n  ")
    ACTIVE_BRANCH = \
        subprocess.run(
            ["git", "branch", "--show-current"], 
            cwd=WORKDIR, 
            capture_output=True,
            text=True,
            shell=True,
        ).stdout.strip()
        
    def __init__(self) -> None:
        super().__init__()
        self.label = f"Version Control ({VersionControl.ACTIVE_BRANCH})"
        self.description = "Pulls the latest changes from the remote repository or switches to a different branch."
        self.category = "Verson Control"
        return
    
    def getParameterInfo(self) -> list:
        branch = arcpy.Parameter(
            displayName="Branch",
            name="branch",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
        )
        branch.value = VersionControl.ACTIVE_BRANCH
        branch.filter.type = "ValueList"
        branch.filter.list = VersionControl.BRANCHES
        
        status = arcpy.Parameter(
            displayName="Status",
            name="status",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
        )
        status.controlCLSID='{E5456E51-0C41-4797-9EE4-5269820C6F0E}'
        status.value = self.get_status()
        
        pull = arcpy.Parameter(
            displayName="Pull",
            name="pull",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )
        pull.value = True
        
        return [branch, pull, status]
    
    def updateParameters(self, parameters: list) -> None:
        params = archelp.Parameters(parameters)
        
        if params.branch.value != VersionControl.ACTIVE_BRANCH:
            params.pull.value = False
            params.pull.enabled = False
        else:
            params.pull.enabled = True
        
        params.status.value = self.get_status()
        
        return
    
    def execute(self, parameters:list, messages:list) -> None:
        params = archelp.Parameters(parameters)
        
        if params.pull.value:
            result =\
                subprocess.run(
                    ["git", "pull"], cwd=VersionControl.WORKDIR, 
                    capture_output=True, 
                    text=True
                )
            archelp.message(result.stdout)
            if result.stderr:
                archelp.message(result.stderr, "error")
        elif VersionControl.ACTIVE_BRANCH != params.branch.value:
            result =\
                subprocess.run(
                    ["git", "checkout", params.branch.value], 
                    cwd=VersionControl.WORKDIR, 
                    capture_output=True, 
                    text=True,
                    shell=True,
                )
            archelp.message(result.stdout)
        archelp.message(self.get_status())
        
    def get_status(self) -> str:
        try:
            status = \
                subprocess.run(
                    ["git", "status"], 
                    cwd=VersionControl.WORKDIR, 
                    capture_output=True,
                    text=True,
                    shell=True,
                ).stdout.strip()
            return status
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"