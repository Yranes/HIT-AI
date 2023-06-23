import util
q = util.PriorityQueue()

a = (1, 2)
b = (2, 3)
c = (3, 4)

q.push(a, 3)
q.push(b, 4)
print(q.heap[0])
q.push(c, 2)

a = [1, 2]
b = a + ["w"]

print(b)