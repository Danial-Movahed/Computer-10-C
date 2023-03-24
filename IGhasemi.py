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

    def Notify(self,name,message):
        print(message)

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
        self.people = list()
    
    def NotifyAll(self, message):
        self.people.Notify(message)

    def createFactor(self, name):
        tmp = Factor(name)
        tmp.dw,tmp.iw,tmp.zw = self.tm.NewFactor(name)
        self.factors[name] = tmp
    def start(self):
        name = self.chooseName()
        dish = self.chooseDish()
        i=0
        flavors = [-1,-1,-1]
        while -1 in flavors:
            flavors[i] = self.chooseFlavor()

    def chooseName(self):
        print("#> Please enter your name:")
        return input()

    def chooseDish(self):
        print("thank you. choose your holder: 1. plastic 2. cone")
        dish = -1
        while dish not in [1,2]:
            dish = int(input())
        return dish

    def chooseFlavor(self,num):
        print(f"choose your #{num+1} flavor: 1. hazelnut 2. strawberry 3. chocolate 4. coffee (0. back)")
        fl = -1
        while fl not in [0,1,2,3,4]:
            fl = int(input())
        return fl

    def run(self):
        self.quit = False
        print("Welcome to iGhasemi icecream shop!")
        while not self.quit:
            cmd = input("Enter your command: ")
            if cmd == "start":
                self.start()
            elif cmd == "help":
                print("start: Start buying process")
            elif cmd == "exit":
                self.quit = True
        print("Bye!")