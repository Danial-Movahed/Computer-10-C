class Inode:
    name: str

    def size() -> int:
        raise NotImplementedError


class File(Inode):
    def __init__(self, name, content) -> None:
        self.name = name
        self.content = content

    def size(self):
        return len(self.content)


class Directory(Inode):
    def __init__(self, name: str, parent: "Directory") -> None:
        self.name: str = name
        self.parent: Directory = parent
        self.selfObj = self
        if self.name == ".." or self.name == ".":
            self.selfObj = parent
        if self.name == "." or self.name == ".." or self.name == "/":
            self.children: list[Inode] = []
            return
        self.children: list[Inode] = [Directory(".",self),Directory("..",self.parent)]

    def size(self):
        s = 4
        for i in self.children:
            s += i.size()
        return s

    def pwd(self):
        if self.name == "/":
            return "/"
        return self.parent.pwd()+self.name+"/"

    def giveObj(self):
        return self.selfObj


class CommandLine:
    def __init__(self) -> None:
        self.quit = False
        self.cwd: Directory = Directory("/", None)

    def mkdir(self, dirName):
        self.cwd.children.append(Directory(dirName, self.cwd))

    def findDir(self, dirName):
        for inode in self.cwd.children:
            if inode.name == dirName:
                return inode
        return False

    def changeDirectory(self, dirName):
        tmp = self.findDir(dirName)
        if not tmp:
            print(f'cd: no such file or directory: {dirName}')
            return
        self.cwd = tmp.giveObj()

    def mkfile(self, fName, content):
        self.cwd.children.append(File(fName, content))

    def pwd(self):
        print(self.cwd.pwd())

    def size(self):
        print(self.cwd.size())

    def ls(self):
        for i in self.cwd.children:
            print(i.name)

    def run(self):
        while not self.quit:
            cmd = input("$ ").split(" ")
            if cmd[0] == "mkdir":
                self.mkdir(cmd[1])
            elif cmd[0] == "cd":
                self.changeDirectory(cmd[1])
            elif cmd[0] == "mkfile":
                self.mkfile(cmd[1], " ".join(cmd[2:]))
            elif cmd[0] == "pwd":
                self.pwd()
            elif cmd[0] == "size":
                self.size()
            elif cmd[0] == "ls":
                self.ls()
            elif cmd[0] == "exit":
                self.quit = True


cmd = CommandLine()
cmd.run()
