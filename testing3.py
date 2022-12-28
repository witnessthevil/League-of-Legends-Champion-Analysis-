the_list = list(range(100))

iter_list = iter(the_list)

for i in range(100):
    print(next(iter_list))



def adding_dict(**reality):
    return sum(reality.values())

dict = {'a':1,"b":2}
tuple = (1,2)

print(adding_dict())