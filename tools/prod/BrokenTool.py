import arcpy

class BrokenTool(object):
    def __init__(self) -> None:
        self.label = "Broken Tool"
        self.description = "My Tool"
        self.category = "Useful Tools"
        
        self.paramA = None
        self.paramB = 1
        return
    
    def getParameterInfo(self) -> list:
        p1 = arcpy.Parameter(
            displayName="Parameter A",
            name="paramA",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p2 = Memory(paramA = self.paramA, paramB = self.paramB)
        
        return [p1, p2]
    
    def updateParameters(self, parameters: list) -> None:
        self.paramA = "Hello World"
        self._memory_hack(pA=self.paramA)
        parameters[0].value = "paramA set to Hello World"
        parameters[1].paramA += " UPDATED"
        parameters[1].paramB += 1
        return
    
    def updateMessages(self, parameters: list) -> None:
        self.paramB = 2
        self._memory_hack(pB=self.paramB)
        parameters[0].setWarningMessage("paramB set to 2")
        parameters[1].paramA += " MESSAGED"
        parameters[1].paramB += 1
        return
    
    def execute(self, parameters: list, messages: list) -> None:
        arcpy.AddMessage(f"{self.paramA=}, expected 'Hello World'")
        arcpy.AddMessage(f"{self.paramB=}, expected 2")
        
        arcpy.AddMessage("\nExecuting Memory Hack...")
        self.paramA, self.paramB = self._memory_hack()
        arcpy.AddMessage(f"{self.paramA=}, expected 'Hello World'")
        arcpy.AddMessage(f"{self.paramB=}, expected 2")
        
        arcpy.AddMessage("\nExecuting Parameter Hack...")
        arcpy.AddMessage(f"{parameters[1]=}")
        arcpy.AddMessage(f"{parameters[1].paramA=}")
        arcpy.AddMessage(f"{parameters[1].paramB=}")
        return
    
    # This is disgusting, don't do this. It relies on a bug in Python's initialization of default arguments to store state because
    # Python toolboxes don't actually update self. variables in updateParameters and updateMessages calls
    def _memory_hack(self, pA=None, pB=None,
                     paramA=[None], paramB=[None]) -> tuple:
        """ DO NOT EVER DO THIS """
        if pA:
            paramA[0] = pA
        if pB:
            paramB[0] = pB
        return (paramA[0], paramB[0])
    
class Memory:
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        return