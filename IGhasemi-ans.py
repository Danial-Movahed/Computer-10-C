########### ICECREAM ###########
class Icecream:
    def __str__(self) -> str:
        return self.__class__.__name__

class HazelnutIcecream(Icecream):
    pass

class ChocolateIcecream(Icecream):
    pass

def icecream_factory(name: str) -> Icecream:
    if name == 'hazelnut':
        return HazelnutIcecream()
    if name == 'chocolate':
        return ChocolateIcecream()

########### TOPPING ###########

class Topping:
    def __str__(self) -> str:
        return self.__class__.__name__

class Jelly(Topping):
    pass

class Dragee(Topping):
    pass

def topping_factory(name: str) -> Topping:
    if name == 'jelly':
        return Jelly()
    if name == 'dragee':
        return Dragee()

########### HOLDER ###########

class Holder:
    def __str__(self) -> str:
        return self.__class__.__name__

class ConeHolder(Holder):
    pass

class PlasticHolder(Holder):
    pass

def holder_factory(name: str) -> Holder:
    if name == 'plastic':
        return PlasticHolder()
    if name == 'cone':
        return ConeHolder()

class Memento:
    def __init__(self, order: 'Order') -> None:
        self.customer = order.customer
        self.holder: Holder = order.holder
        self.icecreams: list[Icecream] = order.icecreams.copy()
        self.topping: Topping = order.topping

class Order:
    def __init__(self, customer: str) -> None:
        self.customer = customer
        self.holder: Holder = None
        self.icecreams: list[Icecream] = []
        self.topping: Topping = None
        self.mementos: list[Memento] = []

    def get_stage(self) -> int:
        if self.holder == None:
            return 0
        elif len(self.icecreams) == 0:
            return 1
        elif len(self.icecreams) == 1:
            return 2
        elif len(self.icecreams) == 2:
            return 3
        elif self.topping == None:
            return 4
        else:
            return 5
        
    def create_memento(self) -> Memento:
        return Memento(self)
    
    def restore_memento(self, memento: Memento):
        self.topping = memento.topping
        self.holder = memento.holder
        self.customer = memento.customer
        self.icecreams = memento.icecreams

class IObserver:
    def get_command():
        raise NotImplementedError

class Worker(IObserver):
    def __init__(self, mr_ghasemi: 'MrGhasemi') -> None:
        self.active_order: Order = None
        self.mr_ghasemi = mr_ghasemi
        self.stages = []

    def assign(self, order: Order):
        self.active_order = order
        self.mr_ghasemi.subscribe(self, order.customer)

    def get_command(self, command: str):
        if command == 'finish':
            self.mr_ghasemi.unsubscribe(self, self.active_order.customer)
            self.active_order == None
        if self.active_order.get_stage() not in self.stages:
            return
        elif command == 'back':
            if len(self.active_order.mementos) == 0:
                return
            last_memento = self.active_order.mementos.pop()
            self.active_order.restore_memento(last_memento)
        else:
            new_memento = self.active_order.create_memento()
            if self.process_command(command) == True:
                self.active_order.mementos.append(new_memento)

            
    def process_command(self, command) -> True:
        pass

class HolderWorker(Worker):
    def __init__(self, mr_ghasemi: 'MrGhasemi') -> None:
        super().__init__(mr_ghasemi)
        self.stages = [0]

    def process_command(self, command: str) -> bool:
        holder = holder_factory(command)
        if holder is None:
            return False
        self.active_order.holder = holder
        return True

class IcecreamWorker(Worker):
    def __init__(self, mr_ghasemi: 'MrGhasemi') -> None:
        super().__init__(mr_ghasemi)
        self.stages = [1,2,3]

    def process_command(self, command: str) -> bool:
        icecream = icecream_factory(command)
        if icecream is not None:
            self.active_order.icecreams.append(icecream)
            return True
        return False

class ToppingWorker(Worker):
    def __init__(self, mr_ghasemi: 'MrGhasemi') -> None:
        super().__init__(mr_ghasemi)
        self.stages = [4,5]

    def process_command(self, command: str) -> bool:
        topping = topping_factory(command)
        if topping is None:
            return False
        self.active_order.topping = topping
        return True

class Fariborz():
    def __init__(self, mr_ghasemi: 'MrGhasemi') -> None:
        self.mr_ghasemi = mr_ghasemi
        self.icecream_workers: list[IcecreamWorker] = []
        self.topping_workers: list[ToppingWorker] = []
        self.holder_workers: list[HolderWorker] = []
        for i in range(10):
            self.holder_workers.append(HolderWorker(mr_ghasemi))
            self.icecream_workers.append(IcecreamWorker(mr_ghasemi))
            self.topping_workers.append(ToppingWorker(mr_ghasemi))

    def handle_new_order(self, order: Order):
        self.choose_worker(self.holder_workers, order)
        self.choose_worker(self.icecream_workers, order)
        self.choose_worker(self.topping_workers, order)

    def choose_worker(self, workers: list[Worker], order: Order):
        while(True):
            for w in workers:
                if w.active_order is None:
                    w.assign(order)
                    return

class MrGhasemi:
    def __init__(self) -> None:
        self.fariborz: Fariborz = Fariborz(self)
        self.subscribers: dict[str, list[IObserver]] = {}

    def new_order(self, name: str) -> Order:
        self.subscribers[name] = []
        order = Order(name)
        self.fariborz.handle_new_order(order)
        return order

    def shout_command(self, customer: str, command: str):
        for observer in self.subscribers[customer]:
            observer.get_command(command)

    def finalize_order(self, customer: str):
        for observer in self.subscribers[customer].copy():
            observer.get_command('finish')

    def subscribe(self, observer: IObserver, customer: str):
        if customer not in self.subscribers.keys():
            self.subscribers[customer] = []
        self.subscribers[customer].append(observer)
    
    def unsubscribe(self, observer: IObserver, customer: str):
        if customer in self.subscribers.keys():
            self.subscribers[customer].remove(observer)

class iGhasemi:
    def __init__(self, mr_ghasemi: MrGhasemi) -> None:
        self.mr_ghasemi = mr_ghasemi
    def run(self):
        name = input("hello. please enter your name: ")
        order = self.mr_ghasemi.new_order(name)
        while(True):
            if order.get_stage() == 0:
                command = input("please enter your holder: ")
                self.mr_ghasemi.shout_command(name, command)
            if order.get_stage() == 1:
                command = input("please enter your icecream 1: ")
                self.mr_ghasemi.shout_command(name, command)
            if order.get_stage() == 2:
                command = input("please enter your icecream 2: ")
                self.mr_ghasemi.shout_command(name, command)
            if order.get_stage() == 3:
                command = input("please enter your icecream 3: ")
                self.mr_ghasemi.shout_command(name, command)
            if order.get_stage() == 4:
                command = input("please enter your topping: ")
                self.mr_ghasemi.shout_command(name, command)
            if order.get_stage() == 5:
                print('this is your order:')
                print("Holder:",order.holder)
                print("Icecreams:",order.icecreams[0], order.icecreams[1], order.icecreams[2])
                print("Topping:",order.topping)
                command = input('do you confirm? ')
                if command == 'yes':
                    self.mr_ghasemi.finalize_order(name)
                    print('done!')
                    break
                else:
                    self.mr_ghasemi.shout_command(name, command)

################# MAIN #################

ghasemi = MrGhasemi()
ighasemi = iGhasemi(ghasemi)
ighasemi.run()