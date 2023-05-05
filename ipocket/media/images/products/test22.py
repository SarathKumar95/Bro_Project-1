

list1 = [1,2,4,5,6,3]

for i in list1:
    for num in (2,i):
        if i % num == 0:
            pass
        else:
            print(num)
            