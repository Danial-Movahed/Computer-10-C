class Sorter:
    @classmethod
    def Sort(cls,l):
        raise NotImplemented()
class PythonSort(Sorter):
    @classmethod
    def Sort(cls,l):
        print("Sorting with python sort")
        l=sorted(l)
        return l[::-1]
class BubbleSort(Sorter):
    @classmethod
    def Sort(cls,l):
        print("Sorting with bubble sort")
        for i in range(len(l)-1):
            for j in range(0,len(l)-i-1):
                if l[j]>l[j+1]:
                    swapped = True
                    l[j],l[j+1] = l[j+1],l[j]
                
            if not swapped:
                return
        return l

class StrategySort:
    def __init__(self,l,sortMethod=None):
        self.sortMethod = sortMethod
        self.l = l

    def __str__(self):
        return str(self.sortMethod(self.l))