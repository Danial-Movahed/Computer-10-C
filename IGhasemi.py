class iWorker:
    currentlyWorkingName: str

    def Notify(self, name: str) -> bool:
        raise NotImplementedError

    def End(self, name: str) -> None:
        raise NotImplementedError


class iTaskMaster:
    pass


class DishWorker(iWorker):
    def __init__(self) -> None:
        self.currentlyWorkingName = None

    def Notify(self, name: str) -> bool:
        if self.isCurrentlyWorking == None:
            print(f"{name}'s dish with me!")
            self.currentlyWorkingName = name
            return True
        return None

    def End(self, name: str) -> None:
        if self.currentlyWorkingName == name:
            self.currentlyWorkingName = None


class IceWorker(iWorker):
    def __init__(self) -> None:
        self.currentlyWorkingName = None

    def Notify(self, name: str) -> bool:
        if self.isCurrentlyWorking == None:
            print(f"{name}'s dish with me!")
            self.currentlyWorkingName = name
            return True
        return False

    def End(self, name: str) -> None:
        if self.currentlyWorkingName == name:
            self.currentlyWorkingName = None


class ZalWorker(iWorker):
    def __init__(self) -> None:
        self.currentlyWorkingName = None

    def Notify(self, name: str) -> bool:
        if self.isCurrentlyWorking == None:
            print(f"{name}'s dish with me!")
            self.currentlyWorkingName = name
            return True
        return False

    def End(self, name: str) -> None:
        if self.currentlyWorkingName == name:
            self.currentlyWorkingName = None

class Factor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.dw = None
        self.iw = None
        self.zw = None

class TaskMaster(iTaskMaster):
    def __init__(self) -> None:
        self.dws = [DishWorker()]*10
        self.iws = [IceWorker()]*10
        self.zws = [ZalWorker()]*10
    
    def NewFactor(self, name):
        return (self.findDishWorker(name),self.findIceWorker(name),self.findZalWorker(name))

    def findDishWorker(self, name):
        for w in self.dws:
            if w.Notify(name):
                return w
        return None
    def findIceWorker(self, name):
        for w in self.iws:
            if w.Notify(name):
                return w
    def findZalWorker(self, name):
        for w in self.zws:
            if w.Notify(name):
                return w
            
class iGhasemi:
    def __init__(self, tm: TaskMaster) -> None:
        self.factors = dict()
        self.tm = tm
    
    def createFactor(self, name):
        tmp = Factor(name)
        tmp.dw,tmp.iw,tmp.zw = self.tm.NewFactor(name)
        self.factors[name] = tmp