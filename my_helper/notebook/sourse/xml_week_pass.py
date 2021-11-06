points = [2, 3]
rows = [3, 4, 5, 6, 1]
res = [[3, 4], [5, 6, 1]]
l = []
prev = 0
cursor = iter(range(14, 100))
for i in range(len(points)):
    l.append(rows[prev:prev+points[i]])
    prev = points[i]
for j in l:
    print("A" + str(next(cursor)))
    for k in range(len(j)):
        for i in range(j[k]):
            if i == 0:
                print("A" + str(next(cursor)))
            else:
                print("a" + str(next(cursor)))