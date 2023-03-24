from Sorting import *
a=[1,4,2,6,3,5,8,7]
s1 = StrategySort(a,PythonSort.Sort)
s2 = StrategySort(a,BubbleSort.Sort)
s3 = StrategySort(a,sorted)
print(s1)
print(s2)
print("With internal Sorted")
print(s3)