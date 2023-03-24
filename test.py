class A:
    count=0
    def __init__(self):
        self.name="Mamad"
    @classmethod
    def a(self):
        print(self.count)
    def b(self):
        print(self.name)
A.a()
b=A()
b.b()

Strategy design pattern