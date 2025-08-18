from collections import deque as dq

#used for FIFO (first in first out)

example = dq()

example.append(1)
example.append(2)
example.append(3)

print(example)

example.popleft()
example.popleft()

print(example)
