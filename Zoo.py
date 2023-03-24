from os import path


class IAnimal:
    typeName: str
    name: str
    isVahshi: bool
    forbiddenCharactersFromName: str

    def setName(self, name: str) -> bool:
        raise NotImplemented()


class ILocalizer:
    def localize(self, message: str) -> str:
        raise NotImplemented()


class IFileHandler:
    def createFile(self) -> None:
        raise NotImplemented()

    def openFile(self) -> None:
        raise NotImplemented()

    def getAnimalList(self) -> list:
        raise NotImplemented()

    def closeFile(self) -> None:
        raise NotImplemented()

    def saveFile(self) -> None:
        raise NotImplemented()


class IZoo:
    def loadAnimals(self) -> None:
        raise NotImplemented

    def printAnimalList(self) -> None:
        raise NotImplemented

    def mainLoop(self) -> None:
        raise NotImplemented


class AhliAnimal(IAnimal):
    forbiddenCharactersFromName = "kytbz"
    isVahshi = False

    def setName(self, name: str) -> bool:
        res = False if any(
            [i in name for i in self.forbiddenCharactersFromName]) else True
        if res:
            self.name = name
            return True
        return False


class VahshiAnimal(IAnimal):
    forbiddenCharactersFromName = "smhp"
    isVahshi = True

    def setName(self, name: str) -> bool:
        res = False if any(
            [i in name for i in self.forbiddenCharactersFromName]) else True
        if res:
            self.name = name
            return True
        return False


class Rabbit(VahshiAnimal):
    typeName = "Rabbit"


class Wolf(VahshiAnimal):
    typeName = "Wolf"


class Tiger(AhliAnimal):
    typeName = "Tiger"


class Cow(AhliAnimal):
    typeName = "Cow"


class PersianLocalizer(ILocalizer):
    localizations = {
        "Rabbit": "خرگوش",
        "Wolf": "گرگ",
        "Tiger": "پلنگ",
        "Cow": "گاو",
        "Add": "اضافه",
        "Delete": "پاک",
        "Exit": "خروج",
        "Invalid command!": "دستور وجود ندارد!",
        "Enter your command: ": "دستوری وارد کنید: ",
        "Enter animal type: ": "نوع حیوان را وارد کنید: ",
        "Please enter the name of the animal: ": "لطفا اسم حیوان را وارد کنید: ",
        "This name is already registered!": "این اسم قبلا ثبت شده است!",
        "The entered name is illegal for this animal!": "اسم وارد شده برای حیوان مورد نظر غیرمجاز است!",
        "This animal is wild and cannot be released!": "این حیوان وحشی است و نمیتواند آزاد شود!",
        "Cannot find any eligible animal with this name!": "هیچ حیوان مناسبی با این اسم پیدا نشد!"
    }

    def localize(self, message: str) -> str:
        return self.localizations[message]


class EnglishLocalizer(ILocalizer):
    def localize(self, message: str) -> str:
        return message


class LangChooser:
    localizers: dict = {
        "English": EnglishLocalizer,
        "Persian": PersianLocalizer
    }

    def __new__(cls, lang: str = "English") -> ILocalizer:
        return cls.localizers[lang]()


class TypeChooser:
    types: dict = {
        "Rabbit": Rabbit,
        "Wolf": Wolf,
        "Tiger": Tiger,
        "Cow": Cow,
        "خرگوش": Rabbit,
        "گرگ": Wolf,
        "پلنگ": Tiger,
        "گاو": Cow
    }

    def __new__(self, typeInp: str) -> IAnimal:
        return self.types[typeInp]()


class Singleton:
    instance = None

    def __new__(cls) -> object:
        if cls.instance == None:
            cls.instance = super().__new__(cls)
        return cls.instance


class FileHandler(Singleton, IFileHandler):
    f = None

    def createFile(self) -> None:
        self.f = open("ZooFile.txt", "w")
        self.f.close()

    def openFile(self) -> None:
        if not path.exists("ZooFile.txt"):
            self.createFile()
        self.f = open("ZooFile.txt", "r")

    def getAnimalList(self) -> list:
        return self.f.readlines()

    def saveFile(self, Animals) -> None:
        self.f.close()
        self.f = open("ZooFile.txt", "w")
        for animal in Animals:
            tmp = animal.typeName + " " + animal.name
            self.f.write(tmp+"\n")

    def closeFile(self) -> None:
        self.f.close()


class Zoo(IZoo):
    def __init__(self, localizer: ILocalizer):
        self.localizer = localizer
        self.fileHandler = FileHandler()
        self.fileHandler.openFile()
        self.Animals = []
        self.quit = False
        self.loadAnimals()
        self.printAnimalList()
        self.mainLoop()

    def loadAnimals(self) -> None:
        animals = self.fileHandler.getAnimalList()
        for animal in animals:
            data = animal.split(" ")
            tmp = TypeChooser(data[0])
            tmp.setName(data[1].strip("\n"))
            self.Animals.append(tmp)

    def printAnimalList(self) -> None:
        for animal in self.Animals:
            print("Type: "+self.localizer.localize(animal.typeName))
            print("name: "+animal.name)
            print("######################")

    def mainLoop(self) -> None:
        while not self.quit:
            cmd = input(self.localizer.localize("Enter your command: "))
            if cmd == self.localizer.localize("Add"):
                animalType = input(
                    self.localizer.localize("Enter animal type: "))
                while not (animalType == self.localizer.localize("Rabbit") or animalType == self.localizer.localize("Cow") or animalType == self.localizer.localize("Tiger") or animalType == self.localizer.localize("Wolf")):
                    animalType = input(
                        self.localizer.localize("Enter animal type: "))
                tmp = TypeChooser(animalType)
                name = input(self.localizer.localize(
                    "Please enter the name of the animal: "))
                for animal in self.Animals:
                    if animal.name == name:
                        print(self.localizer.localize(
                            "This name is already registered!"))
                        continue
                if not tmp.setName(name):
                    print(self.localizer.localize(
                        "The entered name is illegal for this animal!"))
                else:
                    self.Animals.append(tmp)

            elif cmd == self.localizer.localize("Delete"):
                found = False
                name = input(self.localizer.localize(
                    "Please enter the name of the animal: "))
                for animal in self.Animals:
                    if animal.name == name:
                        found = True
                        if animal.isVahshi:
                            print(self.localizer.localize(
                                "This animal is wild and cannot be released!"))
                        else:
                            self.Animals.remove(animal)
                        break
                if not found:
                    print(self.localizer.localize(
                        "Cannot find any eligible animal with this name!"))

            elif cmd == self.localizer.localize("Exit"):
                self.quit = True

            else:
                print(self.localizer.localize("Invalid command!"))
        self.fileHandler.saveFile(self.Animals)
        self.fileHandler.closeFile()


lang: str = input("Please select your language\nPersian/English: ")
while not (lang == "Persian" or lang == "English"):
    lang: str = input("Please select your language\nPersian/English: ")

zoo = Zoo(LangChooser(lang))
