
with open('PSY - GANGNAM STYLE.mp4', 'rb') as file:
    byteA = bytearray()
    while True:
        byte = file.read(1)
        byteA.append(int(byte))
    print(byteA)
"""
x = [1, [1, 2, 3], 2]
y = [[1, [1, 2, 3], 2], [4, [5, 6, 7], 4]]
z = [[3, 4, 5, ], [1, 4, 5], ['path', 1, 2]]
tags = "12.4.21"
# normal has one contained list, multiple  has > 1 list
# if not any(isinstance(el, list) for el in currentEntry):
tags = tags.strip('[]').split(',')
print(type(tags), type(tags[0]))
print(tags)
print(z[len(z) - 1][0])


def countList(x):
    count = 0
    for el in x:
        if isinstance(el, list):
            print('incremented')
            count = count + 1
    return count


if countList(x) == 1:
    print('single entry')
"""
