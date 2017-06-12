fantasy_team = []
fantasy_team.append("frank gore")
print(fantasy_team)
# Prints: ['frank gore']

fantasy_team.append("calvin johnson") 
print(fantasy_team[1])
# Prints: calvin johnson

fantasy_team.remove("calvin johnson") 
fantasy_team[0] = "aaron rodgers"
print(fantasy_team)
# Prints: ['aaron rodgers']


a = [1, 5, 4, 2, 3] 
print(a[0], a[-1])
# Prints: 1, 3

a[4] = a[2] + a[-2]
print(a)
# Prints: 1 5 4 2 6

print(len(a))
# Prints: ?5

print(4 in a)
# Prints: True

a[1] = [a[1], a[0]]
print(a)
# Prints: 1 [5,1]4,2,6 not sure why though

x = [3, 1, 2, 1, 5, 1, 1, 7]
def remove_all(el, lst):
    while el in lst:
        lst.remove(el)
remove_all(1,x)
print(x)


lst = [1, 2, 4, 2, 1]
def add_this_many(x,y,lst):
    c = lst.count(x)
    for i in range(c):
        lst.append(y)

add_this_many(1, 5, lst)
print(lst)
print()

####################
#understanding Slicing
a = [3, 1, 4, 2, 5, 3]
print(a[:4])
# Prints: 3 1 4 2

print(a)
# Prints: 3 1 4 2 5 3

print(a[1::2])
# Prints: 1 2 3

print(a[:])
# Prints: 3 1 4 2 5 3

print(a[4:2])
# Prints: 

print(a[1:-2])
# Prints: 1 4 2

print(a[::-1])
# Prints: 3 5 2 4 1 3

##########################
#Understanding for loops
print()

x = [3, 2, 4, 5, 1]

def reverse(lst):
    print(list(reversed(lst)))

reverse(x)
print()

x = [1, 2, 3, 4, 5]
def rotate(lst,k):
    list_copy = list(lst)
    for i in range(len(lst)):
        if k < 0:
            lst[i+k] = list_copy[i]
        else:
            lst[i] = list_copy[i-k]
rotate(x, 3)
print(x)
print()
##########################
#Understanding Dictonaries

superbowls = {'joe montana': 4, 'tom brady':3, 'joe flacco': 0}
print(superbowls['tom brady'])
# Prints: 3

superbowls['peyton manning'] = 1
print(superbowls)
# Prints: {'peyton manning': 1, 'tom brady': 3, 'joe flacco': 0, 'joe montana': 4}

superbowls['joe flacco'] = 1
print(superbowls)
# Prints:{'peyton manning': 1, 'tom brady': 3, 'joe flacco': 1, 'joe montana': 4}

print('colin kaepernick' in superbowls)
#Prints: False

print(len(superbowls))
#Prints: 4

print(superbowls['peyton manning'] == superbowls['joe montana'])
#Prints: False Becuase 1 != 4

superbowls[('eli manning', 'giants')] = 2
print(superbowls)
#Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 2}

superbowls[3] = 'cat'
print(superbowls)
#Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 2, 3: 'cat'}


superbowls[('eli manning', 'giants')] =  superbowls['joe montana'] + superbowls['peyton manning']
print(superbowls)
#Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 5, 3: 'cat'}

superbowls[('steelers', '49ers')] = 11
print(superbowls)
#Prints: {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 5, 3: 'cat', ('steelers', '49ers'): 11}

################################
#Dictonary Practice

d = {1: {2:3, 3:4}, 2:{4:4, 5:3}}

def replace_all(d,x,y):
    for key in d.keys():
        if type(d[key]) == dict:
            replace_all(d[key], x, y)
        else:
            d[key] = y if d[key] == x else d[key]

replace_all(d, 3, 1)
print(d)
print()

d = {1:2, 2:3, 3:2, 4:3}
def rm(d,x):
    remove_key = [key for key in d.keys() if d[key]==x]
    for key in remove_key:
        del d[key]
rm(d,2)
print(d)

