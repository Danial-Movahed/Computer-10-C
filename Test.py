class asghar:
    def __init__(self,name) -> None:
        self.name = name


class B:
    def __init__(self) -> None:
        pass
    def changeName(self, d):
        d.name = "aaaaaaaaaaaaaa"

class A:
    def __init__(self) -> None:
        self.b = B()
        self.d = {"aa":asghar("mamad"),"bb":asghar("akbar")}
        self.b.changeName(self.d["aa"])
        print(self.d["aa"].name)

a=A()