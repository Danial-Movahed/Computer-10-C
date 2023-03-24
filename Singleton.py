class Singleton():
    instance=None
    def __init__(self):
        self.name = "test"
    def __new__(cls):
        #return super(Singleton, cls).__new__(cls)
        if cls.instance == None:
            cls.instance = super().__new__(cls)
        return cls.instance
singl = Singleton()
newSingl = Singleton()
singl.test = "salaam"
print(newSingl.test)