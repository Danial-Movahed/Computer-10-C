class iPerson:
    def Notify(self, name: str, message: str) -> None:
        raise NotImplementedError


class iWorker(iPerson):
    currentlyWorkingName: str

    def IsFree(self, name: str) -> bool:
        raise NotImplementedError

    def End(self, name: str) -> None:
        raise NotImplementedError


class iTaskMaster(iPerson):
    dws: list[iWorker]
    iws: list[iWorker]
    tws: list[iWorker]

    def NewFactor(self, name: str) -> bool:
        raise NotImplementedError

    def findWorker(self, mode: str, name: str) -> iWorker:
        raise NotImplementedError


class DishWorker(iWorker):
    def __init__(self) -> None:
        self.currentlyWorkingName = None
        self.holder = None

    def Notify(self, name: str, type: str, message: str) -> None:
        print(name, type, message)
        self.holder = message
        if type == "end":
            self.End(name)

    def IsFree(self, name: str) -> bool:
        if self.currentlyWorkingName == None:
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
        self.scopes: list["Scope"] = list()

    def Notify(self, name: str, type: str, message: str) -> None:
        print(name, type, message)
        if not (type == "end" or type == "regrets."):
            self.scopes.append(Scope(message))
        if type == "end":
            self.End(name)

    def IsFree(self, name: str) -> bool:
        if self.currentlyWorkingName == None:
            print(f"{name}'s icecream with me!")
            self.currentlyWorkingName = name
            return True
        return False

    def End(self, name: str) -> None:
        if self.currentlyWorkingName == name:
            self.currentlyWorkingName = None


class TopWorker(iWorker):
    def __init__(self) -> None:
        self.currentlyWorkingName = None
        self.topping = None

    def Notify(self, name: str, type: str, message: str) -> None:
        print(name, type, message)
        self.topping = message
        if type == "end":
            self.End(name)

    def IsFree(self, name: str) -> bool:
        if self.currentlyWorkingName == None:
            print(f"{name}'s topping with me!")
            self.currentlyWorkingName = name
            return True
        return False

    def End(self, name: str) -> None:
        if self.currentlyWorkingName == name:
            self.currentlyWorkingName = None


class Scope:
    def __init__(self, flavor: str) -> None:
        self.flavor = flavor


class Factor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.orderWorkers: OrderWorkers = None
        self.holder = None
        self.scopes: list[Scope] = list()
        self.topping = None
        self.currentStep = "holder"

    def restore(self, snapshot: "Snapshot") -> None:
        self.holder = snapshot.holder
        self.scopes = snapshot.scopes.copy()
        self.topping = snapshot.topping
        self.currentStep = snapshot.currentStep

    def getSnapshot(self) -> "Snapshot":
        return Snapshot(self)


class Snapshot:
    def __init__(self, f: Factor) -> None:
        self.holder = f.holder
        self.scopes = f.scopes.copy()
        self.topping = f.topping
        self.currentStep = f.currentStep


class FactorCareTaker:
    def __init__(self, factor: Factor) -> None:
        self.factor = factor
        self.snapShots: list[Snapshot] = list()

    def _saveSnapshot(self) -> None:
        self.snapShots.append(self.factor.getSnapshot())

    def setHolder(self, holder: str) -> None:
        self._saveSnapshot()
        self.factor.holder = holder
        self.factor.currentStep = "flavor"

    def setScopes(self, flavor: str) -> None:
        self._saveSnapshot()
        self.factor.scopes.append(Scope(flavor))
        if len(self.factor.scopes) == 3:
            self.factor.currentStep = "topping"

    def setTopping(self, topping: str) -> None:
        self._saveSnapshot()
        self.factor.topping = topping
        self.factor.currentStep = "verify"

    def undo(self) -> None:
        if len(self.snapShots) == 0:
            return
        self.factor.restore(self.snapShots.pop())


class OrderWorkers:
    def __init__(self, dw: iWorker, iw: iWorker, tw: iWorker) -> None:
        self.iw, self.dw, self.tw = iw, dw, tw


class TaskMaster(iTaskMaster):

    def __init__(self) -> None:
        self.dws = [DishWorker()]*10
        self.iws = [IceWorker()]*10
        self.tws = [TopWorker()]*10
        self.workerTypes = {
            "ice": self.iws,
            "top": self.tws,
            "dish": self.dws,
        }

    def NewFactor(self, name: str, fct: FactorCareTaker) -> None:
        dw, iw, tw = self.findWorker("dish", name), self.findWorker(
            "ice", name), self.findWorker("top", name)
        fct.factor.orderWorkers = OrderWorkers(dw,iw,tw)

    def findWorker(self, mode: str, name: str) -> iWorker:
        for w in self.workerTypes[mode]:
            if w.IsFree(name):
                return w
        return None


class iGhasemi:
    obj = None

    def __new__(cls,tm) -> "iGhasemi":
        if cls.obj == None:
            cls.obj = super().__new__(cls)
        return cls.obj

    def __init__(self, tm: TaskMaster) -> None:
        self.factors: dict[str, FactorCareTaker] = dict()
        self.tm = tm

    def createFactor(self, name: str) -> None:
        self.factors[name] = FactorCareTaker(Factor(name))
        self.tm.NewFactor(name,self.factors[name])
            
    def Shout(self,name,type,msg):
        if type == "holder":
            self.factors[name].factor.orderWorkers.dw.Notify(name, type, msg)
        elif "flavor" in type:
            self.factors[name].factor.orderWorkers.iw.Notify(name, type, msg)
        elif type == "topping":
            self.factors[name].factor.orderWorkers.dw.Notify(name, type, msg)
        else:
            self.factors[name].factor.orderWorkers.dw.Notify(name, type, msg)
            self.factors[name].factor.orderWorkers.tw.Notify(name, type, msg)
            self.factors[name].factor.orderWorkers.iw.Notify(name, type, msg)

    def start(self) -> None:
        name = self.chooseName()
        self.createFactor(name)
        while self.factors[name].factor.currentStep != "end":
            if self.factors[name].factor.currentStep == "holder":
                choice = self.chooseDish()
                self.factors[name].setHolder(choice)
                self.Shout(name, "holder", choice)

            elif self.factors[name].factor.currentStep == "flavor":
                choice = self.chooseFlavor(
                    len(self.factors[name].factor.scopes))
                if not self.processChoice(choice, name):
                    continue
                self.factors[name].setScopes(choice)
                self.Shout(name, f"flavor #{len(self.factors[name].factor.scopes)}", choice)

            elif self.factors[name].factor.currentStep == "topping":
                choice = self.chooseTopping()
                if not self.processChoice(choice, name):
                    continue
                self.factors[name].setTopping(choice)
                self.Shout(name, "topping", choice)

            elif self.factors[name].factor.currentStep == "verify":
                choice = self.chooseVerify(name)
                if not self.processChoice(choice, name):
                    continue
                self.factors[name].factor.currentStep = "end"
                self.Shout(name, "end", "")
        print("#> Done")

    def processChoice(self, choice: str, name: str) -> bool:
        if choice == "back":
            self.factors[name].undo()
            self.Shout(name, "regrets.", "")
            self.factors[name].factor.orderWorkers.dw.holder = self.factors[name].factor.holder
            self.factors[name].factor.orderWorkers.iw.scopes = self.factors[name].factor.scopes.copy()
            self.factors[name].factor.orderWorkers.tw.topping = self.factors[name].factor.topping
            return False
        return True

    def chooseVerify(self, name: str) -> str:
        print("#> this is your final order. do you confirm? (yes, back)")
        print(f"\t- holder: {self.factors[name].factor.holder}")
        print(
            f"\t- scopes: {', '.join([x.flavor for x in self.factors[name].factor.scopes])}")
        print(f"\t- topping: {self.factors[name].factor.topping}")
        choice = ""
        while choice not in ["yes", "back"]:
            choice = input("choice: ")
        return choice

    def chooseName(self) -> str:
        print("#> please enter your name:")
        return input()

    def chooseDish(self) -> str:
        print("#> thank you. choose your holder: plastic, cone")
        dish = ""
        while dish not in ["plastic", "cone"]:
            dish = input("choice: ")
        return dish

    def chooseFlavor(self, num: str) -> str:
        print(
            f"#> choose your #{num+1} flavor: hazelnut, strawberry, chocolate, coffee (back)")
        fl = ""
        while fl not in ["hazelnut", "strawberry", "chocolate", "coffee", "back"]:
            fl = input("choice: ")
        return fl

    def chooseTopping(self) -> str:
        print("#> choose your topping: confetti, jelly, chocolate syrup (back)")
        tp = ""
        while tp not in ["confetti", "jelly", "chocolate syrup", "back"]:
            tp = input("choice: ")
        return tp

    def run(self) -> None:
        self.quit = False
        print("Welcome to iGhasemi icecream shop!")
        while not self.quit:
            cmd = input("Enter your command: ")
            if cmd == "start":
                self.start()
            elif cmd == "help":
                print("start: Start buying process")
                print("exit: Exit iGhasemi icecream shop")
                print("help: Show this message")
            elif cmd == "exit":
                self.quit = True
        print("Bye!")


fariborz = TaskMaster()
ghasemi = iGhasemi(fariborz)
ghasemi.run()
