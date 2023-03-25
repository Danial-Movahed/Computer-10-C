class iPerson:
    def Notify(self, message):
        raise NotImplementedError


class iWorker(iPerson):
    currentlyWorkingName: str

    def IsFree(self, name: str) -> bool:
        raise NotImplementedError

    def End(self, name: str) -> None:
        raise NotImplementedError


class iTaskMaster(iPerson):
    pass


class DishWorker(iWorker):
    def __init__(self) -> None:
        self.currentlyWorkingName = None

    def Notify(self, message):
        print(message)

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

    def Notify(self, message):
        print(message)

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

    def Notify(self, message):
        print(message)

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
    def __init__(self, flavor) -> None:
        self.flavor = flavor


class Factor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.holder = None
        self.scopes: list[Scope] = list()
        self.topping = None
        self.currentStep = "holder"

    def restore(self, snapshot):
        self.holder = snapshot.holder
        self.scopes = snapshot.scopes
        self.topping = snapshot.topping
        self.currentStep = snapshot.currentStep

    def getSnapshot(self):
        return Snapshot(self)


class Snapshot:
    def __init__(self, f: Factor) -> None:
        self.holder = f.holder
        self.scopes = f.scopes
        self.topping = f.topping
        self.currentStep = f.currentStep


class FactorCareTaker:
    def __init__(self, factor: Factor) -> None:
        self.factor = factor
        self.snapShots: list[Snapshot] = list()

    def _saveSnapshot(self):
        self.snapShots.append(self.factor.getSnapshot())

    def setHolder(self, holder):
        self._saveSnapshot()
        self.factor.holder = holder
        self.factor.currentStep = "flavor"

    def setScopes(self, flavor):
        self._saveSnapshot()
        self.factor.scopes.append(Scope(flavor))
        if len(self.factor.scopes) == 3:
            self.factor.currentStep = "topping"

    def setTopping(self, topping):
        self._saveSnapshot()
        self.factor.topping = topping
        self.factor.currentStep = "verify"

    def undo(self):
        if len(self.snapShots) == 0:
            return
        self.factor.restore(self.snapShots.pop())


class OrderWorkers:
    def __init__(self, dw, iw, tw) -> None:
        self.iw, self.dw, self.tw = iw, dw, tw


class TaskMaster(iTaskMaster):
    def __init__(self) -> None:
        self.dws = [DishWorker()]*10
        self.iws = [IceWorker()]*10
        self.tws = [TopWorker()]*10
        self.workersInProgress = dict()

    def NewFactor(self, name):
        dw = self.findDishWorker(name)
        iw = self.findIceWorker(name)
        tw = self.findTopWorker(name)
        if dw and iw and tw:
            self.workersInProgress[name] = OrderWorkers(dw, iw, tw)
            return True
        return False

    def Notify(self, message):
        print(message)
        message = message.split()
        if message[1] == "end":
            self.workersInProgress[message[0]].dw.End(message[0])
            self.workersInProgress[message[0]].iw.End(message[0])
            self.workersInProgress[message[0]].tw.End(message[0])

    def findDishWorker(self, name):
        for w in self.dws:
            if w.IsFree(name):
                return w
        return False

    def findIceWorker(self, name):
        for w in self.iws:
            if w.IsFree(name):
                return w
        return False

    def findTopWorker(self, name):
        for w in self.tws:
            if w.IsFree(name):
                return w
        return False


class iGhasemi:
    def __init__(self, tm: TaskMaster) -> None:
        self.factors: dict[str, FactorCareTaker] = dict()
        self.tm = tm
        self.people = list()

    def addPeople(self, person):
        self.people.append(person)

    def Shout(self, message):
        for p in self.people:
            p.Notify(message)

    def createFactor(self, name):
        if self.tm.NewFactor(name):
            self.factors[name] = FactorCareTaker(Factor(name))

    def start(self):
        name = self.chooseName()
        self.createFactor(name)
        while self.factors[name].factor.currentStep != "end":
            if self.factors[name].factor.currentStep == "holder":
                choice = self.chooseDish()
                self.factors[name].setHolder(choice)
                self.Shout(f"{name} holder {choice}")

            elif self.factors[name].factor.currentStep == "flavor":
                choice = self.chooseFlavor(
                    len(self.factors[name].factor.scopes))
                if not self.processChoice(choice, name):
                    continue
                self.factors[name].setScopes(choice)
                self.Shout(
                    f"{name} #{len(self.factors[name].factor.scopes)} flavor {choice}")

            elif self.factors[name].factor.currentStep == "topping":
                choice = self.chooseTopping()
                if not self.processChoice(choice, name):
                    continue
                self.factors[name].setTopping(choice)
                self.Shout(f"{name} topping {choice}")

            elif self.factors[name].factor.currentStep == "verify":
                choice = self.chooseVerify(name)
                if not self.processChoice(choice, name):
                    continue
                self.factors[name].factor.currentStep = "end"
                self.Shout(f"{name} end")
        print("#> Done")
    def processChoice(self, choice, name):
        if choice == "back":
            print("aaaa")
            self.factors[name].undo()
            self.Shout(f"{name} regrests.")
            return False
        return True

    def chooseVerify(self, name):
        print("#> this is your final order. do you confirm? (yes, back)")
        print(f"\t- holder: {self.factors[name].factor.holder}")
        print(f"\t- scopes: {', '.join([x.flavor for x in self.factors[name].factor.scopes])}")
        print(f"\t- topping: {self.factors[name].factor.topping}")
        choice = ""
        while choice not in ["yes","back"]:
            choice = input("choice: ")

    def chooseName(self):
        print("#> please enter your name:")
        return input()

    def chooseDish(self):
        print("#> thank you. choose your holder: plastic, cone")
        dish = ""
        while dish not in ["plastic", "cone", "back"]:
            dish = input("choice: ")
        return dish

    def chooseFlavor(self, num):
        print(
            f"#> choose your #{num+1} flavor: hazelnut, strawberry, chocolate, coffee (back)")
        fl = ""
        while fl not in ["hazelnut", "strawberry", "chocolate", "coffee", "back"]:
            fl = input("choice: ")
        return fl

    def chooseTopping(self):
        print("#> choose your topping: confetti, jelly, chocolate syrup (back)")
        tp = ""
        while tp not in ["confetti", "jelly", "chocolate syrup", "back"]:
            tp = input("choice: ")
        return tp

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


fariborz = TaskMaster()
ghasemi = iGhasemi(fariborz)
ghasemi.addPeople(fariborz)
ghasemi.run()
