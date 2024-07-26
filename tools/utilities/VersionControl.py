import arcpy
import subprocess
import os
from pathlib import Path
from typing import Literal

from utils.datamodel.tool import Tool
import utils.funcs.archelp as archelp
from utils.funcs.archelp import print

class VersionControl(Tool):
    __slots__ = ["active_branch", "branches", "workdir"]
    
    def __init__(self) -> None:
        super().__init__()
        
        self.workdir: os.PathLike = Path(__file__).parents[2].absolute()
        self.active_branch: str = self.get_active_branch()
        self.branches: list[str] = self.get_branches()
              
        self.label = f"Version Control ({self.active_branch})"
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
        branch.value = self.active_branch
        branch.filter.type = "ValueList"
        branch.filter.list = self.branches
        
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
        
        if params.branch.value != self.active_branch:
            params.pull.value = False
            params.pull.enabled = False
        else:
            params.pull.enabled = True
        
        params.status.value = self.get_status()
        return
    
    def execute(self, parameters:list, messages:list) -> None:
        params = archelp.Parameters(parameters)
        
        if params.pull.value:
            print(self.git_subprocess("pull", None, self.workdir).stdout)
        elif self.active_branch != params.branch.value:
            print(self.git_subprocess("checkout", params.branch.value, self.workdir).stdout)
        print(self.get_status())
        
    def get_status(self) -> str:
        return self.git_subprocess("status", None, self.workdir).stdout.strip()
    
    def get_branches(self) -> list[str]:
        return self.parse_git_branches(self.git_subprocess("branch", "-a", self.workdir).stdout)
    
    def get_active_branch(self) -> str:
        return self.git_subprocess("branch", "--show-current", self.workdir).stdout.strip()
    
    @staticmethod
    def git_subprocess(command: Literal["branch", "pull", "checkout", "status"], 
                   flag: Literal["-a", "--show-current"] | str | None,
                   cwd: os.PathLike = None) -> subprocess.CompletedProcess:
        """ Run a git command using subprocess """
        result = subprocess.run(
            ["git", command] + ([flag] if flag else []), 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            shell=True,
        )
        return result
    
    @staticmethod
    def parse_git_branches(git_branches: str) -> list:
        """ Parse the output of 'git branch -a' """
        return [branch.strip().replace('*', '').lstrip() for branch in git_branches.strip().split('\n')]
