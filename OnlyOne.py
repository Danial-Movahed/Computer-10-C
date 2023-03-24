class IShiriniGiver:
    def give_shirini(self, code: int) -> None:
        raise NotImplemented()


class Single:
    instance = None

    def __new__(cls):
        if cls.instance == None:
            cls.instance = super().__new__(cls)
        return cls.instance


class MrMohammadi(Single):
    def get_shirini(self, teacher: IShiriniGiver) -> None:
        code = random.randint(1, 3)
        teacher.give_shirini(code)


class MrMahdavi(IShiriniGiver):
    def give_shirini(self, code: int) -> None:
        if code == 1:
            tmp = "danmarki"
        elif code == 2:
            tmp = "rollet"
        elif code == 3:
            tmp = "yazdi"
        print("Here you go, "+tmp)


class MrAhmadi():
    def _be_sakhti_give_shirini(self, name: str) -> None:
        print("Here you go, "+name)


class MrAhmadiAdapter(IShiriniGiver):
    mrAhmadi = MrAhmadi()

    def give_shirini(self, code: int) -> None:
        if code == 1:
            tmp = "danmarki"
        elif code == 2:
            tmp = "rollet"
        elif code == 3:
            tmp = "yazdi"
        self.mrAhmadi._be_sakhti_give_shirini(tmp)
