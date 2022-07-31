times = int(input())
list2 = []

for i in range(times):
    a = input().split(' ')
    list1 = list(map(int, a))
    list2 += list1
    list2.sort()

for answ in list2:
    print(answ, end=' ')