class Worker:
    def __init__(self, nxt):
        self._nxt = nxt

    def handle(self):
        self.processRequest()
        if self._nxt != None:
            self._nxt.handle()

    def processRequest(self):
        raise NotImplementedError()

class StickerWorker(Worker):
    def processRequest(self):
        print("Sticker is sticked!")

class CleanWorker(Worker):
    def processRequest(self):
        print("Cleaned up!")

class NoteWorker(Worker):
    def processRequest(self):
        print("Noted the id!")

class CheckWorker(Worker):
    def processRequest(self):
        print("Everything looks fine!")

class EndWorker(Worker):
    def processRequest(self):
        print("The end!")


class Naghale(Worker):
    def __init__(self, nxt, handler):
        self._nxt = nxt
        self.handler = handler

    def processRequest(self):
        self.handler.handle()

class Main:
    def __init__(self) -> None:
        self.mainNaghale: Worker = Naghale(None, StickerWorker(NoteWorker(CleanWorker(Naghale(CheckWorker(EndWorker(None)),StickerWorker(NoteWorker(CheckWorker(CleanWorker(None)))))))))
    def process(self) -> None:
        self.mainNaghale.handle()

main = Main()
main.process()