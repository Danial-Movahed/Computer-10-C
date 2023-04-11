class Item:
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price


class Package(Item):
    def __init__(self, name: str, price: int = 5) -> None:
        self.name = name
        self.items = []
        self.price = price


class cli:
    def __init__(self) -> None:
        self.quit = False
        self.sumPrice = 0
        self.items: list[Item] = []
        self.run()

    def addItem(self, name: str, price: int) -> None:
        self.items.append(Item(name, price))
        self.sumPrice += price

    def printSum(self) -> None:
        print(self.sumPrice)

    def pack(self, items: list[Item], name: str) -> None:
        self.sumPrice += 5
        try:
            items.remove("none")
        except ValueError:
            pass
        tmp = Package(name)
        for i in items:
            for c in self.items:
                if c.name == i:
                    self.items.remove(c)
                    tmp.items.append(c)
                    break
        self.items.append(tmp)
    
    def printPack(self, items: list[Item]) -> None:
        for c in items:
            if type(c) == Package:
                print(c.name)
                print("{")
                self.printPack(c.items)
        for c in items:
            if type(c) != Package:
                print(c.name)
        print("}")

    def run(self) -> None:
        while not self.quit:
            cmd = input("Enter your command: ").split(" ")
            if cmd[0] == "pack":
                self.pack(cmd[1:-1],cmd[-1])
            elif cmd[0] == "add":
                self.addItem(cmd[1],int(cmd[2]))
            elif cmd[0] == "sum":
                self.printSum()
            elif cmd[0] == "printpack":
                print("{")
                self.printPack(self.items)
            elif cmd[0] == "exit":
                self.quit = True
        print("Bye!")

Shop=cli()
